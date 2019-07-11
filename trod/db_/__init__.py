import warnings

from trod import errors
from trod.db_.connpool import Pool
from trod.db_.executer import fetch, execute
from trod.model_ import loader


__all__ = (
    'Connector',
    'Doer',
)


class Connector:

    __slots__ = ()

    _pool = None

    @classmethod
    def pool(cls):
        if cls._pool is None:
            raise errors.NoConnectorError(
                "Connector has not been created, maybe you should call \
                `trod.bind()` before."
            )
        return cls._pool

    @classmethod
    async def create(cls, *args, **kwargs):

        # TODO test
        if cls._pool is not None:
            raise RuntimeError()

        if args or kwargs.get('url'):
            cls._pool = await Pool.from_url(*args, **kwargs)
        else:
            cls._pool = await Pool(*args, **kwargs)

    @classmethod
    async def close(cls):

        if cls._pool:
            cls._pool = await cls._pool.close()
            return True

        warnings.warn('No binding db connector or closed', errors.ProgrammingWarning)
        return False

    @classmethod
    def state(cls):
        if cls._pool:
            return cls._pool.state
        return None


class Doer:

    __slots__ = ('_model', '_sql', '_args')

    def __init__(self, model, sql=None, args=None):
        self._model = model
        self._sql = sql or []
        self._args = args

    def __str__(self):
        args = f' % {self._args}' if self._args else ''
        return f"Doer by {Connector.pool()}\n For SQL({self.sql}{args})"

    __repr__ = __str__

    @property
    def sql(self):
        if isinstance(self._sql, (list, tuple)):
            self._sql.append(';')
            self._sql = ' '.join(self._sql)
        return self._sql

    async def do(self):

        pool = Connector.pool()

        if getattr(self, '_select', False):
            fetch_results = await fetch(pool, self.sql, args=self._args)
            return loader.load(self._model, fetch_results, use_td=self._use_td)
        exec_results = await execute(
            pool, self.sql, values=self._args, is_batch=getattr(self, '_batch', False)
        )
        return loader.ExecResults(*exec_results)
