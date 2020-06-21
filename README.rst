====
helo
====

🌎 [`English </README.rst>`_] ∙ [`简体中文 </README.CN.rst>`_]

.. image:: https://img.shields.io/pypi/v/helo.svg
        :target: https://pypi.python.org/pypi/helo

.. image:: https://travis-ci.org/at7h/helo.svg?branch=master
        :target: https://travis-ci.org/at7h/helo

.. image:: https://coveralls.io/repos/github/at7h/helo/badge.svg?branch=master
        :target: https://coveralls.io/github/at7h/helo?branch=master

.. image:: https://app.codacy.com/project/badge/Grade/c68578653eb546488fadddd95f19939c
        :target: https://www.codacy.com/manual/at7h_/helo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=at7h/helo&amp;utm_campaign=Badge_Grade

.. image:: https://img.shields.io/pypi/pyversions/helo
        :target: https://img.shields.io/pypi/pyversions/helo
        :alt: PyPI - Python Version

🌟 **Helo** is a simple and small low-level asynchronous ORM using Python asyncio_.
It is very intuitive and easy to use.

Helo can help you easily build expressive common SQL statements in your asynchronous applications.
You only need to use friendly object-oriented APIs to manipulate data without caring about the details of SQL statement writing and data processing. 
Suitable for scenarios where the business logic structure is relatively simple and has a certain amount of concurrency.

* Requires: Python 3.7+
* Now only supports MySQL
* Not supports table relationship

Quickstart
----------

See the wiki_ page for more information and quickstart_ documentation.


Installation
------------

.. code-block:: console

    $ pip install helo

See the installation_ wiki page for more options.


Basic Examples
--------------

First, you should to import the ``Helo`` and instantiate a global variable:

.. code-block:: python

    import helo

    db = helo.G()


Defining models is simple:

.. code-block:: python

    class User(db.Model):
        id = helo.BigAuto()
        name = helo.VarChar(length=45, null=False)
        email = helo.Email(default='')
        password = helo.VarChar(length=100, null=False)
        create_at = helo.Timestamp(default=helo.ON_CREATE)


    class Post(db.Model):
        id = helo.Auto()
        title = helo.VarChar(length=100)
        author = helo.Int(default=0)
        content = helo.Text(encoding=helo.ENCODING.utf8mb4)
        create_at = helo.Timestamp(default=helo.ON_CREATE)
        update_at = helo.Timestamp(default=helo.ON_UPDATE)


Show some basic examples:

.. code-block:: python

    import asyncio
    from datetime import datetime


    async def show_case():

        # Binding the database(creating a connection pool)
        # and create the table:
        await db.bind('mysql://user:password@host:port/db')
        await db.create_tables([User, Post])

        # Inserting few rows:

        user = User(name='at7h', password='1111')
        user_id = await user.save()
        print(user_id)  # 1

        users = await User.get(user_id)
        print(user.id, user.name)  # 1, at7h

        await User.update(email='g@gmail.com').where(User.id == user_id).do()

        ret = await User.insert(name='pope', password='2222').do()
        posts = [
            {'title': 'Python', 'author': 1},
            {'title': 'Golang', 'author': 2},
        ]
        ret = await Post.minsert(posts).do()
        print(ret)  # (2, 1)

        # Supports expressive and composable queries:

        count = await User.select().count()
        print(count) # 2

        # Last gmail user
        user = await User.select().where(
            User.email.endswith('gmail.com')
        ).order_by(
            User.create_at.desc()
        ).first()
        print(user) # [<User object> at 1]

        # Using `helo.adict`
        users = await User.select(
            User.id, User.name
        ).where(
            User.id < 2
        ).all(wrap=False)
        print(user)  # [{'id': 1, 'name': 'at7h'}]

        # Paginate get users who wrote Python posts this year
        users = await User.select().where(
            User.id.in_(
                Post.select(Post.author).where(
                    Post.update_at > datetime(2019, 1, 1),
                    Post.title.contains('Python')
                ).order_by(
                    Post.update_at.desc()
                )
            )
        ).paginate(1, 10)
        print(users) # [<User object> at 1]

        # How many posts each user wrote?
        user_posts = await User.select(
            User.name, helo.F.COUNT(helo.SQL('1')).as_('posts')
        ).join(
            Post, helo.JOINTYPE.LEFT, on=(User.id == Post.author)
        ).group_by(
            User.name
        ).rows(100)

    asyncio.run(show_case())

👉 See `more examples </examples>`_


Contributing 👏
---------------

I hope those who are interested can join in and work together.

Any kind of contribution is expected:
report a bug 🐞, give a advice or create a pull request 🙋‍♂️.


Thanks 🤝
---------

* Special thanks to projects aiomysql_ and peewee_, helo uses aiomysql_ (as the MySQL connection driver),
  and referenced peewee_ in program design.
* Please feel free to ⭐️ this repository if this project helped you 😉!

.. _wiki: https://github.com/at7h/helo/wiki
.. _quickstart: https://github.com/at7h/helo/wiki#quickstart
.. _installation: https://github.com/at7h/helo/wiki#installation
.. _asyncio: https://docs.python.org/3.7/library/asyncio.html
.. _aiomysql: https://github.com/aio-libs/aiomysql
.. _peewee: https://github.com/coleifer/peewee
