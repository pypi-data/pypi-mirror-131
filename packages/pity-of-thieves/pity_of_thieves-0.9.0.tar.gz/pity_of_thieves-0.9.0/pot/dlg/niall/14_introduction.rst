:author:    D E Haynes
:made_at:   2021-12-07
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

.. entity:: ITEM
   :types:  pot.world.Item
   :states: pot.types.Engagement.static

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

Here in |LOCN_ARTICLE| |LOCN_NAME|, |PLAYER_NAME| meets |NPC_NAME|.

He's a young man in his late teens, solidly built.
He is one of the Tithingmen, who patrol the homesteads and try to keep order.

He carries a light spear, which he plants in the ground as he pauses to talk.

.. property:: NPC.state 1
.. property:: NPC.state pot.types.Engagement.static
.. property:: DRAMA.prompt Press Return to talk with |NPC_NAME|

Second look
-----------

.. condition:: NPC.state 1

[NPC]_

    Hi, |PLAYER_NAME|, can you do me a favour?

[PLAYER]_

    Sure.

[NPC]_

    Can you give this to Freda for me?

He holds out what seems to be a |ITEM_AKA| of some kind.

.. property:: NPC.state 2
.. property:: DRAMA.prompt Type a command to continue.

Give
----

.. condition:: ITEM.holder.name |NPC_NAME|

|NPC_NAME| gives |PLAYER_NAME| the |ITEM_NAME|.

.. property:: ITEM.holder PLAYER

Gave
----

.. condition:: ITEM.holder.name |PLAYER_NAME|

|ITEM_HOLDER| looks down at the |ITEM_NAME| he's holding.

|NPC_NAME| continues on his patrol.


.. property:: ITEM.holder PLAYER
.. property:: NPC.state pot.types.Engagement.acting

.. |PLAYER_NAME| property:: PLAYER.name
.. |NPC_NAME| property:: NPC.name
.. |ITEM_NAME| property:: ITEM.names[0].noun
.. |ITEM_AKA| property:: ITEM.names[1].noun
.. |ITEM_HOLDER| property:: ITEM.holder.names[0].noun
.. |LOCN_NAME| property:: LOCAL.names[0].noun
.. |LOCN_ARTICLE| property:: LOCAL.names[0].article.definite
