:author:    D E Haynes
:made_at:   2021-11-30
:project:   The Pity of Thieves
:dwell: 0.2
:pause: 0.9

.. entity:: PLAYER
   :types:  pot.world.Character
   :states: pot.types.Engagement.player

.. entity:: LOCAL
   :types:  pot.world.Location

.. entity:: RAT
   :types:  pot.world.Character
   :states: pot.world.Spot.woodshed

.. entity:: DRAMA
   :types:  balladeer.Drama
   :states: pot.types.Operation.prompt

.. entity:: SETTINGS
   :types:  balladeer.Settings

Exploration
===========

beggars_ash_0
-------------

.. condition:: LOCAL.state pot.world.Spot.beggars_ash
.. condition:: LOCAL.state 0

{0}

|PLAYER_SPOT| is a clearing by the road as it winds North.
A large dead tree, white and split open, gives this place a name.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

beggars_ash_1
-------------

.. condition:: LOCAL.state pot.world.Spot.beggars_ash
.. condition:: LOCAL.state 1

{0}

All there is at |PLAYER_SPOT| is a large dead tree, white and split open.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

beggars_ash_2
-------------

.. condition:: LOCAL.state pot.world.Spot.beggars_ash
.. condition:: LOCAL.state 2

{0}

There is nothing for |PLAYER_NAME| in |PLAYER_SPOT|. No need to go on further.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

bridge_street_0
---------------

.. condition:: LOCAL.state pot.world.Spot.bridge_street
.. condition:: LOCAL.state 0

{0}

Up to now, the path has been strewn with rushes to keep down the mud.
Here it is a wooden boardwalk, which becomes a bridge across the river.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

bridge_street_1
---------------

.. condition:: LOCAL.state pot.world.Spot.bridge_street
.. condition:: LOCAL.state 1

{0}

|PLAYER_SPOT| leads to a gate, and beyond that the bridge across the river.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

bridge_street_2
---------------

.. condition:: LOCAL.state pot.world.Spot.bridge_street
.. condition:: LOCAL.state 2

{0}

There is a gate at the end of |PLAYER_SPOT|, to hold the animals before they come to Market.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

butchers_row_0
--------------

.. condition:: LOCAL.state pot.world.Spot.butchers_row
.. condition:: LOCAL.state 0

{0}

No one yet is around at |PLAYER_SPOT|, although it can get busy.
The beasts which are not sold at Market end up here.

The whole place reeks of flesh. Even now in the wintry morning, there is a carnal stench
from every muddy puddle.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

butchers_row_1
--------------

.. condition:: LOCAL.state pot.world.Spot.butchers_row
.. condition:: LOCAL.state 1

{0}

In |PLAYER_SPOT|, long wooden trestles are set up either side of the street.
There are frames for hanging the meat, and big butts for blood and offal.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

butchers_row_2
--------------

.. condition:: LOCAL.state pot.world.Spot.butchers_row
.. condition:: LOCAL.state 2

{0}

The straw underfoot is filthy, bound with dung and blood.
|PLAYER_SPOT| is not a place to hang around.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

cutthroat_lane_0
----------------

.. condition:: LOCAL.state pot.world.Spot.cutthroat_lane
.. condition:: LOCAL.state 0

{0}

|PLAYER_NAME| takes a moment to stop and listen. There is a Woodpecker somewhere
above. His knocking echoes around the trees here on |PLAYER_SPOT|.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

cutthroat_lane_1
----------------

.. condition:: LOCAL.state pot.world.Spot.cutthroat_lane
.. condition:: LOCAL.state 1

{0}

|PLAYER_SPOT| climbs and winds between ancient trees.
Here and there are pathways off to remote dwellings.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

cutthroat_lane_2
----------------

.. condition:: LOCAL.state pot.world.Spot.cutthroat_lane
.. condition:: LOCAL.state 2

{0}

|PLAYER_SPOT| is a little-used track which runs from the North Gate.
It can take you back into the town if you go far enough.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

dingwood_0
----------

.. condition:: LOCAL.state pot.world.Spot.dingwood
.. condition:: LOCAL.state 0

{0}

|PLAYER_NAME| rarely ventures down this way. It is the road
South, past |PLAYER_SPOT|.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

dingwood_1
----------

.. condition:: LOCAL.state pot.world.Spot.dingwood
.. condition:: LOCAL.state 1

{0}

Further in this direction the road passes through the green hills of |PLAYER_SPOT|.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

dingwood_2
----------

.. condition:: LOCAL.state pot.world.Spot.dingwood
.. condition:: LOCAL.state 2

{0}

Looking South. There is nothing beyond for miles.

|PLAYER_NAME| has gone to |PLAYER_SPOT|.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

gardens_0
---------

.. condition:: LOCAL.state pot.world.Spot.gardens
.. condition:: LOCAL.state 0

{0}

|PLAYER_NAME| checks around him as he enters the |PLAYER_SPOT|.
He's been chased out of here many times.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

gardens_1
---------

.. condition:: LOCAL.state pot.world.Spot.gardens
.. condition:: LOCAL.state 1

{0}

The |PLAYER_SPOT| is a pleasant spot away from the town.

It is marked out by oaken posts, bound with iron.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

gardens_2
---------

.. condition:: LOCAL.state pot.world.Spot.gardens
.. condition:: LOCAL.state 2

{0}

A gravel path splits the |PLAYER_SPOT| in two.
At regular intervals there are wooden boxes with decorative grasses and fragrant herbs.

It is tended by some of the old people of the town in return for alms.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

market_0
--------

.. condition:: LOCAL.state pot.world.Spot.market
.. condition:: LOCAL.state 0

{0}

It is so early, that no one is yet at the |PLAYER_SPOT|.

It is a square stockade. There is a single-barred fence at waist height.
Behind that a shamble of stout cages and pens.

The whole assembly is a baffling maze; some pathways blocked by
barrels or toolboxes or coils of heavy hemp roping.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

market_1
--------

.. condition:: LOCAL.state pot.world.Spot.market
.. condition:: LOCAL.state 1

{0}

The |PLAYER_SPOT| is a square stockade. There is a solid fence at waist height.
Behind that a shamble of stout cages and pens.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

market_2
--------

.. condition:: LOCAL.state pot.world.Spot.market
.. condition:: LOCAL.state 2

{0}

The |PLAYER_SPOT| is a baffling maze; some pathways blocked by
barrels and coils of heavy hemp ropes.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

market_house_0
--------------

.. condition:: LOCAL.state pot.world.Spot.market_house
.. condition:: LOCAL.state 0

{0}

The |PLAYER_SPOT| is a favourite spot for |PLAYER_NAME| whenever he can
spare the time to go there.

He loves watching the merchants banter and argue, the auctioneer call for bids,
and the cryer announce the names of defaulters.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

market_house_1
--------------

.. condition:: LOCAL.state pot.world.Spot.market_house
.. condition:: LOCAL.state 1

{0}

The |PLAYER_SPOT| is raised on stout pillars. The ground floor is just a plinth of stone,
with steep steps leading up above.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

market_house_2
--------------

.. condition:: LOCAL.state pot.world.Spot.market_house
.. condition:: LOCAL.state 2

{0}

|PLAYER_NAME| has never seen inside the upper floor of the |PLAYER_SPOT|.
He knows important people meet there, because he watches them come and go.

The merchants and drovers are summoned here every month before Dolphus the Reeve.
At Christmas comes the Aeldorman, Simon of Dene.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

mordiford_quay_0
----------------

.. condition:: LOCAL.state pot.world.Spot.mordiford_quay
.. condition:: LOCAL.state 0

{0}

|PLAYER_NAME| knows the little river well. Since a little boy, he would go to Mordiford
bridge to swim and fish.

Downstream of there is |PLAYER_SPOT|. A jetty built on a gravel spit where the boats
pull up and unload.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

mordiford_quay_1
----------------

.. condition:: LOCAL.state pot.world.Spot.mordiford_quay
.. condition:: LOCAL.state 1

{0}

|PLAYER_SPOT| sits below the confluence of two rivers. There is a great
jetty there, where boats tie up and unload.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

mordiford_quay_2
----------------

.. condition:: LOCAL.state pot.world.Spot.mordiford_quay
.. condition:: LOCAL.state 2

{0}

Piled up all along |PLAYER_SPOT| are goods of every kind. The are barrels of drink, bags of grain
and crates of all sizes, full of produce.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

north_gate_0
------------

.. condition:: LOCAL.state pot.world.Spot.north_gate
.. condition:: LOCAL.state 0

{0}


|PLAYER_NAME| has wandered up to |PLAYER_SPOT|.

There is no real gate here, only two iron-bound posts to mark the edge of the town.
A carved board welcomes travellers from the North.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

north_gate_1
------------

.. condition:: LOCAL.state pot.world.Spot.north_gate
.. condition:: LOCAL.state 1

{0}

|PLAYER_SPOT|.

There is no real gate here, only two iron-bound posts to mark the edge of the town.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

north_gate_2
------------

.. condition:: LOCAL.state pot.world.Spot.north_gate
.. condition:: LOCAL.state 2

{0}

|PLAYER_SPOT|. A carved board welcomes travellers from the North.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

orchard_0
---------

.. condition:: LOCAL.state pot.world.Spot.orchard
.. condition:: LOCAL.state 0

{0}

As a boy, |PLAYER_NAME| loved to come to the |PLAYER_SPOT| and swing from
the low branches of the apple trees.

He would keep a safe distance from the pigs.
They will chase away an intruder from their windfall.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

orchard_1
---------

.. condition:: LOCAL.state pot.world.Spot.orchard
.. condition:: LOCAL.state 1

{0}

It is Winter, and the branches of the |PLAYER_SPOT| are bare.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

orchard_2
---------

.. condition:: LOCAL.state pot.world.Spot.orchard
.. condition:: LOCAL.state 2

{0}

Here in the |PLAYER_SPOT| there are several pigs who shamble about among the trees.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

ross_road_0
-----------

.. condition:: LOCAL.state pot.world.Spot.ross_road
.. condition:: LOCAL.state 0

{0}

Away south and to the west runs the |PLAYER_SPOT|.
It snakes for many miles over bluffs and through valleys until it reaches the deep Forest.

This is a way to Mordiford.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

ross_road_1
-----------

.. condition:: LOCAL.state pot.world.Spot.ross_road
.. condition:: LOCAL.state 1

{0}

Away south and to the west runs the |PLAYER_SPOT|.

This is a way to Mordiford.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

ross_road_2
-----------

.. condition:: LOCAL.state pot.world.Spot.ross_road
.. condition:: LOCAL.state 2

{0}

Away south and to the west runs the |PLAYER_SPOT|.

It snakes for many miles over bluffs and through valleys until it reaches the deep Forest.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

south_end_0
-----------

.. condition:: LOCAL.state pot.world.Spot.south_end
.. condition:: LOCAL.state 0

{0}

Away from the working part of town is |PLAYER_SPOT|.

The dwellings here are larger than elsewhere.

Old families with wealth and standing.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

south_end_1
-----------

.. condition:: LOCAL.state pot.world.Spot.south_end
.. condition:: LOCAL.state 1

{0}

Away from the working part of town is |PLAYER_SPOT|.

The dwellings here are larger than elsewhere.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

south_end_2
-----------

.. condition:: LOCAL.state pot.world.Spot.south_end
.. condition:: LOCAL.state 2

{0}

Away from the working part of town is |PLAYER_SPOT|.

Old families with wealth and standing.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tavern_0
--------

.. condition:: LOCAL.state pot.world.Spot.tavern
.. condition:: LOCAL.state 0

{0}

It is quiet this morning in the |PLAYER_SPOT|. No fire yet in the grate.

The sound of shifting and cleaning in the room at the back.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tavern_1
--------

.. condition:: LOCAL.state pot.world.Spot.tavern
.. condition:: LOCAL.state 1

{0}

The |PLAYER_SPOT| welcomes anyone with a coin.

If not, you can get out.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

tavern_2
--------

.. condition:: LOCAL.state pot.world.Spot.tavern
.. condition:: LOCAL.state 2

{0}

From the beams of the |PLAYER_SPOT| hang carvings of the old Gods.

There are benches against the wall and several barrels on the dirt floor to serve as tables.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

top_cross_0
-----------

.. condition:: LOCAL.state pot.world.Spot.top_cross
.. condition:: LOCAL.state 0

{0}

The road widens out to a broad thoroughfare, where meet several paths through the houses.
This is the spot called |PLAYER_SPOT|.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

top_cross_1
-----------

.. condition:: LOCAL.state pot.world.Spot.top_cross
.. condition:: LOCAL.state 1

{0}

The road at this point is a broad thoroughfare.

From |PLAYER_SPOT| you can look back down the hill into town.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

top_cross_2
-----------

.. condition:: LOCAL.state pot.world.Spot.top_cross
.. condition:: LOCAL.state 2

{0}

The road at this point is a broad thoroughfare.

There are routes from here out into the country.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_street_e_0
----------------

.. condition:: LOCAL.state pot.world.Spot.tower_street_e
.. condition:: LOCAL.state 0

{0}

Tower Street proceeds straight eastward. Here it is clean and well ordered.
The way is paved with stone chippings and cobbles, neatly aranged.

|PLAYER_NAME| smells smoke from some of the buildings as folk begin to stir.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_street_e_1
----------------

.. condition:: LOCAL.state pot.world.Spot.tower_street_e
.. condition:: LOCAL.state 1

{0}

Tower Street proceeds straight eastward.

The way is paved with stone chippings and cobbles, neatly aranged.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

tower_street_e_2
----------------

.. condition:: LOCAL.state pot.world.Spot.tower_street_e
.. condition:: LOCAL.state 2

{0}

Tower Street proceeds straight eastward.

Here it is clean and well ordered.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_street_0
--------------

.. condition:: LOCAL.state pot.world.Spot.tower_street
.. condition:: LOCAL.state 0

{0}

|PLAYER_NAME| envies the folk in |PLAYER_SPOT|.

Here people meet with friends to swap news.

This is where all the scandal and gossip comes from.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_street_1
--------------

.. condition:: LOCAL.state pot.world.Spot.tower_street
.. condition:: LOCAL.state 1

{0}

|PLAYER_SPOT| is narrow at this point, just near the Tavern.

Here people meet with friends to swap news.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

tower_street_2
--------------

.. condition:: LOCAL.state pot.world.Spot.tower_street
.. condition:: LOCAL.state 2

{0}

|PLAYER_SPOT| is narrow at this point, just near the Tavern.

This is where all the scandal and gossip comes from.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_street_w_0
----------------

.. condition:: LOCAL.state pot.world.Spot.tower_street_w
.. condition:: LOCAL.state 0

{0}

At this point are placed several big bundles of cut straw. People coming from
the Market can scrape off the mud before they go on up the street.

Beneath is mostly stone. Cobbles and chippings make for firm footing.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_street_w_1
----------------

.. condition:: LOCAL.state pot.world.Spot.tower_street_w
.. condition:: LOCAL.state 1

{0}

This is the easter end of Tower Street.

This street is made straight and well-paved with stone.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

tower_street_w_2
----------------

.. condition:: LOCAL.state pot.world.Spot.tower_street_w
.. condition:: LOCAL.state 2

{0}

This is the Easter end of Tower Street.

No animals are permitted here. There are thick posts placed close together to keep them out.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_wall_0
------------

.. condition:: LOCAL.state pot.world.Spot.tower_wall
.. condition:: LOCAL.state 0

{0}

The cobbles of Tower Street were left over from the constructioon of the Tower itself.

This place was built by an ancient power. That power bides here still.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

tower_wall_1
------------

.. condition:: LOCAL.state pot.world.Spot.tower_wall
.. condition:: LOCAL.state 1

{0}

|PLAYER_NAME| has no business beyond the |PLAYER_SPOT|.

It's not good to be here for too long.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

tower_wall_2
------------

.. condition:: LOCAL.state pot.world.Spot.tower_wall
.. condition:: LOCAL.state 2

{0}

The Tower dominates the town, and can be seen for miles around.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

yard_0
------

.. The best building logs are traditionally cut near a new moon in the Winter.

.. condition:: LOCAL.state pot.world.Spot.yard
.. condition:: LOCAL.state 0

{0}

The |PLAYER_SPOT| is damp and hung with mist. Stacks of
logs line the way out into the town.

It is Winter and the |PLAYER_SPOT| has been busy.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1
.. property:: RAT.state pot.types.Engagement.acting

yard_1
------

.. condition:: LOCAL.state pot.world.Spot.yard
.. condition:: LOCAL.state 1

{0}

In the |PLAYER_SPOT|.

The wood piles are neat and evenly spaced.
The largest logs over a foot in diameter.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

yard_2
------

.. condition:: LOCAL.state pot.world.Spot.yard
.. condition:: LOCAL.state 2

{0}

In the |PLAYER_SPOT|.

The green is kept separate from the dead.
All sorted according to bow, grain and taper.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

woodshed_0
----------

.. condition:: LOCAL.state pot.world.Spot.woodshed
.. condition:: LOCAL.state 0

{0}

The |PLAYER_SPOT| is stacked nearly full of logs and kindling.
It isn't easy to tell where the wood ends and the shed begins.

There is one space kept clear, and in it a wooden cot and a sort of shelf.

Around the floor are bits of debris; bark and rodent droppings.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

woodshed_1
----------

.. condition:: LOCAL.state pot.world.Spot.woodshed
.. condition:: LOCAL.state 1

{0}

The |PLAYER_SPOT| is stacked nearly full of logs and kindling.
The bundles of wood help to block the gaps in the wall panels.

|PLAYER_NAME| keeps a space clear for sleeping.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 2

woodshed_2
----------

.. condition:: LOCAL.state pot.world.Spot.woodshed
.. condition:: LOCAL.state 2

{0}

The |PLAYER_SPOT| is draughty but dry. There is thatch in the roof space.

Around the floor are bits of debris; bark and rodent droppings.


{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1

Hurry
-----

.. condition:: PLAYER.in_transit True

{0}

|PLAYER_NAME| hurries past |PLAYER_SPOT|.

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

Fallback
--------

{0}

|PLAYER_SPOT|.

{exits}

.. fx:: pot.img |SPOT_NAME|.png
   :offset: 1
   :duration: 3

.. property:: LOCAL.state 1


.. |PLAYER_NAME| property:: PLAYER.name
.. |PLAYER_SPOT| property:: PLAYER.spot.title
.. |SPOT_NAME| property:: PLAYER.spot.name
