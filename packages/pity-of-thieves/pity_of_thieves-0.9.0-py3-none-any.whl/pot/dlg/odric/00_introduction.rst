:author:    D E Haynes
:made_at:   2021-11-30
:project:   The Pity of Thieves
:dwell: 0.2
:pause: 0.9

.. entity:: PLAYER
   :types:  pot.world.Character
   :states: pot.types.Engagement.player
            0

.. entity:: LOCAL
   :types:  pot.world.Location

.. entity:: RAT
   :types:  pot.world.Character
   :states: pot.types.Engagement.hidden
            pot.types.Proximity.present

.. entity:: POISON
   :types:  pot.world.Item
   :states: pot.types.Engagement.hidden
            pot.world.Spot.woodshed

.. entity:: DRAMA
   :types:  balladeer.Drama
   :states: pot.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Introduction
============

Open
----

.. condition:: PLAYER.state pot.world.Spot.woodshed
.. condition:: LOCAL.state 0

Can you hear the sound of Rooks at dawn?

If not, allow your browser to play audio and `begin again </>`_.

That cackle sounds like mockery. They are harsh critics of anyone still in bed.

So wakes |PLAYER_NAME|.

He is in the |PLAYER_SPOT|. Where he sleeps, and when not sleeping, where he works.

.. fx:: pot.mp3  crow_call-3s.mp3
   :offset: 0
   :duration: 3000
   :loop: 1

.. property:: DRAMA.prompt Type 'look'. Or 'help' for other commands.
.. property:: LOCAL.state 1

Listen
------

.. condition:: PLAYER.state pot.world.Spot.woodshed
.. condition:: LOCAL.state 1

{0}

|PLAYER_NAME| listens for a moment. The Rooks are settling down again.

{exits}

.. fx:: pot.mp3  crow_call-3s.mp3
   :offset: 0
   :duration: 3000
   :loop: 1

.. property:: LOCAL.state 2

Bored
-----

.. condition:: PLAYER.state pot.world.Spot.woodshed
.. condition:: LOCAL.state 2

|PLAYER_NAME| isn't doing anything. He looks toward the door.

{exits}

.. property:: LOCAL.state 0
.. property:: PLAYER.state 1
.. property:: DRAMA.prompt Type a command to continue.

.. |PLAYER_NAME| property:: PLAYER.name
.. |PLAYER_SPOT| property:: PLAYER.spot.title
.. |SPOT_NAME| property:: PLAYER.spot.name
