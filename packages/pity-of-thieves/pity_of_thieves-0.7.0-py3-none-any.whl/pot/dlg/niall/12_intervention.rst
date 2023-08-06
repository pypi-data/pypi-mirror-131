:author:    D E Haynes
:made_at:   2021-11-30
:project:   The Pity of Thieves
:dwell:     0
:pause:     0

.. entity:: PLAYER
   :types:  pot.world.Character
   :states: pot.types.Engagement.player

.. entity:: LOCAL
   :types:  pot.world.Location

.. entity:: DRAMA
   :types:  balladeer.Drama
   :states: pot.types.Operation.paused

.. entity:: SETTINGS
   :types:  balladeer.Settings


Intervention
============

Help
----

.. condition:: DRAMA.history[0].name do_help

[DRAMA]_

    The dialogue may give you hints on what you might wish to do.
    Here are some commands to try:

{0}

[DRAMA]_

    You can always choose to do nothing, simply by pressing *Return*.

.. property:: DRAMA.prompt ?
.. property:: DRAMA.state pot.types.Operation.prompt

History
-------

.. condition:: DRAMA.history[0].name do_history

[DRAMA]_

    Recent commands:

{0}

.. property:: DRAMA.state pot.types.Operation.prompt

Inspect Character
-----------------

.. condition:: DRAMA.history[0].name do_inspect_character

[DRAMA]_

    |INPUT_TEXT|

{0}

.. property:: DRAMA.state pot.types.Operation.prompt

Inspect Item
------------

.. condition:: DRAMA.history[0].name do_inspect_item

[DRAMA]_

    |INPUT_TEXT|

{0}

.. property:: DRAMA.state pot.types.Operation.prompt

Look
----

.. condition:: DRAMA.history[0].name do_look

[DRAMA]_

    |PLAYER_NAME| is by |LOCN_ARTICLE| |LOCN_NAME|.
    Looking around, |PLAYER_SUBJECT| is aware of:

{0}

{exits}

.. property:: DRAMA.state pot.types.Operation.prompt

.. |INPUT_TEXT| property:: DRAMA.input_text
.. |PLAYER_NAME| property:: PLAYER.name
.. |LOCN_NAME| property:: LOCAL.names[0].noun
.. |LOCN_ARTICLE| property:: LOCAL.names[0].article.definite
.. |PLAYER_POSS| property:: PLAYER.names[0].pronoun.genitive
.. |PLAYER_SUBJECT| property:: PLAYER.names[0].pronoun.subject
