====
trod 
====

.. image:: https://img.shields.io/pypi/v/trod.svg
        :target: https://pypi.python.org/pypi/trod

.. image:: https://travis-ci.org/at7h/trod.svg?branch=master
        :target: https://travis-ci.org/at7h/trod

.. image:: https://codecov.io/gh/at7h/trod/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/at7h/trod

.. image:: https://img.shields.io/pypi/pyversions/trod.svg
        :target: https://img.shields.io/pypi/pyversions/trod.svg

.. image:: https://img.shields.io/pypi/l/trod.svg
        :target: https://img.shields.io/pypi/l/trod.svg


🌻 **Trod** is a simple asynchronous Python ORM. 
Now it only supports MySQL and uses aiomysql_ as the access 'driver' for the database.

* Strictly, trod is not an ORM, it just working in an ORM-like mode. 
  The objects in trod is completely isolated from the data in the database. 
  It is only a Python object in memory, changing it does not affect the database. 
  You must explicitly execute the commit request to the database.

* Trod uses model and object APIs to compose SQL statements and submit 
  them to the database when executed. When loaded, the data is retrieved 
  from the database and then packaged into objects. 
  Of course, you can also choose other data loading methods


Installation
------------

.. code-block:: console

    pip install trod


Basic Example
-------------

.. code-block:: python

    import asyncio

    from trod import Trod, types


    db = Trod()

    class User(db.Model):

        id = types.Auto()
        name = types.VarChar(length=45)
        password = types.VarChar(length=100)
        create_at = types.Timestamp(default=types.ON_CREATE)
        update_at = types.Timestamp(default=types.ON_UPDATE)


    async show_case():

        await db.bind('mysql://user:password@host:port/db')

        await User.create()

        user = User(name='at7h', password='123456')
        ret = await user.save()
        user = await User.get(ret.last_id)
        print(user.password)  # 123456

        await User.insert(name='guax', password='654321').do()

        async for user in User:
            if user.name == 'at7h':
                assert user.name == '123456'

        user = await User.select().order_by(User.create_at.desc()).first()
        print(user.password) # 654321

        await db.unbind()

    asyncio.run(show_case())


About
-----
at7h is a junior Pythoner, and trod has a lot of temporary 
solutions to optimize and continue to add new features, this is just the beginning 💪.
welcome your issues and pull requests.


Requirements
------------

* Python 3.7+

.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _aiomysql: https://github.com/aio-libs/aiomysql
.. _QuickStart: https://github.com/acthse/trod/blob/master/docs/doc.md
