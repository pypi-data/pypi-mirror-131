:author:    D E Haynes
:made_at:   2021-12-16
:project:   The Pity of Thieves
:dwell: 0.2
:pause: 0.9

.. entity:: PLAYER
   :types:  pot.world.Character
   :states: pot.types.Engagement.player

.. entity:: NPC
   :types:  pot.world.Character
   :states: pot.types.Proximity.present

.. entity:: LOCAL
   :types:  pot.world.Location

.. entity:: DRAMA
   :types:  balladeer.Drama
   :states: pot.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Introduction
============

First impression
----------------

.. condition:: NPC.state 0

It seems to |PLAYER_NAME| at first that there's no one around.
Then, here in |LOCN_ARTICLE| |LOCN_NAME|, he spots |NPC_NAME|.

She's over in the back, sweeping the floor before people arrive.
She flicks her head to clear a lock of long red hair away from her face.

She sees |PLAYER_NAME| and stops.

.. property:: NPC.state 1
.. property:: NPC.state pot.types.Engagement.static
.. property:: DRAMA.prompt Press Return to talk with |NPC_NAME|

Second look
-----------

.. condition:: NPC.state 1

[NPC]_

    Hi |PLAYER_NAME|, you can come in if you don't steal anything.

.. property:: NPC.state 2
.. property:: DRAMA.prompt Type a command to continue.

Busy
----

.. condition:: NPC.state 2

[NPC]_

    I'm busy though, |PLAYER_NAME|. What do you want?

.. property:: NPC.state 1

.. |PLAYER_NAME| property:: PLAYER.name
.. |NPC_NAME| property:: NPC.name
.. |ITEM_NAME| property:: ITEM.names[0].noun
.. |ITEM_AKA| property:: ITEM.names[1].noun
.. |ITEM_HOLDER| property:: ITEM.holder.names[0].noun
.. |LOCN_NAME| property:: LOCAL.names[0].noun
.. |LOCN_ARTICLE| property:: LOCAL.names[0].article.definite
