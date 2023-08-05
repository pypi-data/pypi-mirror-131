zarenacord
===========

A modern, easy to use, feature-rich, and async ready API wrapper for Discord written in Python.

|

.. image:: https://discord.com/api/guilds/456574328990072838/embed.png
   :target: `Support Server`_
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/zarenacord.svg
   :target: https://pypi.python.org/pypi/zarenacord
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/zarenacord.svg
   :target: https://pypi.python.org/pypi/zarenacord
   :alt: PyPI supported Python versions
.. image:: https://readthedocs.org/projects/zarenacord/badge/?version=latest
   :target: http://zarenacord.readthedocs.io/?badge=latest
   :alt: Documentation Status

|

**PLEASE NOTE: This is a fork of OG** |discord.py|_ **by** |Rapptz!|_ **Since Danny no longer maintains dpy so I created this lib in order to add any upcoming feature from Discord**
**and I'm using** |Maya|_ **slash command wrapper for application commands.**

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Command extension to aid with bot creation
- Easy to use with an object oriented design
- 100% coverage of the supported Discord API.
- Optimised in both speed and memory.

Installing
----------

**Python 3.8 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U zarenacord

    # Windows
    py -3 -m pip install -U zarenacord

Otherwise to get voice support you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "zarenacord[voice]"

    # Windows
    py -3 -m pip install -U zarenacord[voice]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/Zarenalabs/zarenacord.git
    $ cd zarenacord
    $ python3 -m pip install -U .[voice]


Optional Packages
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (for voice support)

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)

Quick Example
--------------

.. code:: py

    import discord

    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged in as', self.user)

        async def on_message(self, message):
            # don't respond to ourselves
            if message.author == self.user:
                return

            if message.content == 'ping':
                await message.channel.send('pong')

    client = MyClient()
    client.run('token')

Bot Example
~~~~~~~~~~~~~

.. code:: py

    import discord
    from discord.ext import commands

    bot = commands.Bot(command_prefix='!')

    @bot.command()
    async def ping(ctx):
        await ctx.send('pong')

    bot.run('token')

Application Commands Example
-----------------------------
``zarena`` defines a bot subclass to automatically handle posting updated commands to discords api. This isn't required but highly recommended to use.

.. code:: py

    class MyBot(zarena.Bot):
        def __init__(self):
            super().__init__(command_prefix="!")  # command prefix only applies to message based commands

            self.load_extension("cogs.my_cog")  # important!
            
    if __name__ == '__main__':
        MyBot().run("token")

**Sample cog:**

.. code:: py

    class MyCog(zarena.ApplicationCog):

        # slash command
        @zarena.slash_command()  
        async def slash(self, ctx: zarena.Context, number: int):
            await ctx.send(f"You selected #{number}!", ephemeral=True)
        
        #  message context menus
        @zarena.message_command(name="Quote")
        async def quote(self, ctx: zarena.Context, message: discord.Message):
            await ctx.send(f'> {message.clean_content}\n- {message.author}')
        
        # user context menus
        @zarena.user_command(name='Cookie')
        async def cookie(self, ctx: zarena.Context, user: discord.Member):
            await ctx.send(f'{ctx.author} gave cookie to {user} 🍪')

Links
------

Documentation_ | `Support Server`_ | `Discord API`_

.. _Documentation: https://zarenacord.readthedocs.io/en/latest/index.html
.. _`Support Server`: https://discord.gg/SwfNRrmr3p
.. _`Discord API`: https://discord.gg/discord-api

.. _discord.py: https://github.com/Rapptz/discord.py
.. |discord.py| replace:: **discord.py** 
.. _Rapptz!: https://github.com/Rapptz
.. |Rapptz!| replace:: **Rapptz!**
.. _Maya: https://github.com/XuaTheGrate
.. |Maya| replace:: **Maya's**
