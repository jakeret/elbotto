=============================
El botto del Jasso
=============================

A Python Jass client bot skeleton for the Zuhlke Jass Bot challenge (https://github.com/webplatformz/challenge)

This client allows you to easily develop a bot for the Jass challenge.

---------------
Wiki (Server):
---------------

https://github.com/webplatformz/challenge/wiki

https://jass-challenge.zuehlke.io/



=============================
Start hacking
=============================

---------------
Overview
---------------
This client skeleton has a very simple structure and the code should be easily understood.

To start immediately check fo the comment **CHALLENGE2017**. Here you can implement your logic or see what's important.


You can freely change the structure at anytime to suite your concept of a decent bot implementation.


---------------
Start your own tournament
---------------
To test your bot against other bots, such das the random bot, you need to start your own tournament:

1. checkout, build and start the  `challenge server <https://github.com/webplatformz/challenge>`_  ::

    $ npm install
    $ npm start

2. Browse to http://localhost:3000
3. Enter some user name
4. Enter some tournament name and press **Enter**
5. Join your bots, they should appear on the next page
6. Join random strategy bots for testing. In your challenge server directory enter the command:
`npm run bot:start`
This will add 4 random bot teams to your tournament.


Starting 4 bot to see them on the tournament page pic below::

    $ node build/client/app.js ws://127.0.0.1:3000 Bot_Team_A
    $ node build/client/app.js ws://127.0.0.1:3000 Bot_Team_A
    $ node build/client/app.js ws://127.0.0.1:3000 Bot_Team_B
    $ node build/client/app.js ws://127.0.0.1:3000 Bot_Team_B
