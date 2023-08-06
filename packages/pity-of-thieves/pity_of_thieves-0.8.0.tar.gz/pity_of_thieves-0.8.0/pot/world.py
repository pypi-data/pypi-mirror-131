#!/usr/bin/env python3
# encoding: utf-8

# This is a parser-based text adventure.
# Copyright (C) 2021 D E Haynes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import enum
from collections import deque

from balladeer import Grouping
from balladeer import Stateful
from balladeer import Named
from balladeer import World as WorldType
from balladeer.cartography import Compass
from balladeer.cartography import Map as MapType
from balladeer.cartography import Transit as TransitType
from balladeer.cartography import Via
from balladeer.cartography import Waypoint
from balladeer.speech import Article
from balladeer.speech import Name
from balladeer.speech import Pronoun

from pot.types import Engagement
from pot.types import Operation


class Transit(Named, TransitType): pass


class Map(MapType):

    spots = {
        "beggars_ash":  ["beggars ash"],
        "bridge_street":  ["bridge street", "bridge st"],
        "butchers_row":  ["butchers' row", "butchers row"],
        "cutthroat_lane":  ["cut throat lane", "cutthroat lane"],
        "dingwood":  ["dingwood"],
        "gardens":  ["public gardens", "garden"],
        "market":  ["market"],
        "market_house":  ["market house"],
        "mordiford_quay":  ["mordiford quay", "quay"],
        "north_gate":  ["north gate", "northgate"],
        "orchard":  ["the orchard", "orchard"],
        "ross_road":  ["ross road", "ross rd"],
        "south_end":  ["south end", "southend"],
        "tavern":  ["tavern"],
        "top_cross":  ["top cross"],
        "tower_street_e":  ["upper tower street", "tower st e"],
        "tower_street":  ["tower street", "tower st"],
        "tower_street_w":  ["lower tower street", "tower st w"],
        "tower_wall":  ["tower wall"],
        "yard":  ["yard", "wood yard"],
        "woodshed":  ["wood shed", "woodshed", "shed"],
    }

    Into = enum.Enum("Into", spots, type=Waypoint)
    Exit = enum.Enum("Exit", spots, type=Waypoint)
    Spot = enum.Enum("Spot", spots, type=Waypoint)

    def __init__(self, exit=None, into=None, **kwargs):
        super().__init__(exit, into, **kwargs)
        exit, into = self.exit, self.into

        self.transits = [
            Transit(names=[Name("Road")]).set_state(exit.north_gate, Compass.N, into.beggars_ash, Via.bidir),
            Transit(names=[Name("Orchard Lane")]).set_state(exit.north_gate, Compass.W, into.orchard, Via.bidir),
            Transit(
                names=[Name("Shed door"), Name("Door")]
            ).set_state(exit.yard, Compass.E, into.woodshed, Via.bidir),
            Transit(names=[]).set_state(exit.yard, Compass.N, into.north_gate, Via.bidir),
            Transit(names=[]).set_state(exit.butchers_row, Compass.N, into.yard, Via.bidir),
            Transit(names=[Name("Muddy way")]).set_state(exit.butchers_row, Compass.E, into.market, Via.bidir),
            Transit(names=[]).set_state(exit.butchers_row, Compass.S, into.top_cross, Via.bidir),
            Transit(names=[]).set_state(exit.butchers_row, Compass.W, into.bridge_street, Via.bidir),
            Transit(names=[]).set_state(exit.market, Compass.E, into.tower_street_w, Via.bidir),
            Transit(names=[]).set_state(exit.market, Compass.S, into.market_house, Via.bidir),
            Transit(names=[]).set_state(exit.top_cross, Compass.E, into.market_house, Via.bidir),
            Transit(names=[]).set_state(exit.top_cross, Compass.S, into.south_end, Via.bidir),
            Transit(names=[]).set_state(exit.top_cross, Compass.SW, into.ross_road, Via.bidir),
            Transit(names=[]).set_state(exit.ross_road, Compass.SW, into.mordiford_quay, Via.bidir),
            Transit(names=[]).set_state(exit.south_end, Compass.S, into.dingwood, Via.bidir),
            Transit(names=[]).set_state(exit.tower_street_w, Compass.E, into.tower_street, Via.bidir),
            Transit(names=[]).set_state(exit.tower_street, Compass.E, into.tower_street_e, Via.bidir),
            Transit(
                names=[Name("Oak door"), Name("Door")]
            ).set_state(exit.tower_street, Compass.N, into.tavern, Via.bidir),
            Transit(names=[]).set_state(exit.tower_street_e, Compass.E, into.tower_wall, Via.bidir),
            Transit(names=[]).set_state(exit.tower_street_e, Compass.N, into.gardens, Via.bidir),
            Transit(names=[]).set_state(exit.gardens, Compass.NE, into.cutthroat_lane, Via.bidir),
            Transit(
                names=[Name("Woodland path"), Name("Path")]
            ).set_state(exit.cutthroat_lane, Compass.W, into.north_gate, Via.bidir),
        ]

Into = Map.Into
Exit = Map.Exit
Spot = Map.Spot


class Located(Stateful):

    @property
    def spot(self):
        return self.get_state(Spot)


class Mobile(Located):

    @property
    def in_transit(self):
        return (self.get_state(Into)
            and self.get_state(Into).name != self.get_state(Spot).name
        )


class Character(Named, Mobile): pass
class Item(Named, Located): pass
class Location(Named, Located): pass

# When dropped, items pass to a Location.
# But when Trigger is reset, they revert to being held by their home-spot Location.


class World(WorldType):

    def __init__(self, map_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map = map_

    def build(self):
        for spot in Spot:
            bits = spot.name.split("_")
            article = Article("the", "a") if len(bits) == 1 or bits[-1] == "house" else Article("", "")
            yield Location(names=[Name(i.title(), article) for i in spot.value]).set_state(spot)

        yield from [
            Character(
                names=[Name("Odric", Article("", ""), Pronoun("he", "him", "himself", "his"))],
                description="{0.names[0].noun} is a scruffy little orphan."
            ).set_state(Engagement.player, Spot.woodshed),
            Character(
                names=[Name("Niall", Article("", ""), Pronoun("he", "him", "himself", "his"))],
                description="{0.names[0].noun} is a fit young man with long hair and wild eyes.",
                patrol=deque([Into.south_end, Into.north_gate])
            ).set_state(Engagement.acting, Spot.south_end, Into.north_gate),
            Character(
                names=[Name("Freda", Article("", ""), Pronoun("she", "her", "herself", "her"))],
                description="{0.names[0].noun} is a tall girl, graceful and fair."
            ).set_state(Engagement.acting, Spot.tavern),
            Character(
                names=[Name("Iysla", Article("", ""), Pronoun("she", "her", "herself", "her"))],
                description="{0.names[0].noun} is sharp and nimble. Because she's a Rat."
            ).set_state(Engagement.hidden, Spot.woodshed),
            Character(
                names=[Name("Gerod", Article("", ""), Pronoun("he", "him", "himself", "his"))],
                description="{0.names[0].noun} is a lean, gnarly man."
            ).set_state(Engagement.acting, Spot.beggars_ash),
        ]

        yield from [
            Item(
                names=[Name("Arsenic"), Name("Poison"), Name("Granules")],
                description="A small waxed leather bag, full of crunchy white granules.",
                holder=next(iter(self.lookup["woodshed"]))
            ).set_state(Engagement.hidden, Spot.woodshed),
            Item(
                names=[Name("Knife"), Name("Seax")],
                description="A hefty blade. A tool rather than a weapon; it has a plain wooden handle.",
                holder=next(iter(self.lookup["orchard"]))
            ).set_state(Engagement.static, Spot.orchard),
            Item(
                names=[Name("Cheese"), Name("Food")],
                description="A chunk of hard {0.names[0].noun}, about the size of a fist.",
                holder=next(iter(self.lookup["tavern"]))
            ).set_state(Engagement.static, Spot.tavern),
            Item(
                names=[Name("Briony"), Name("flower")],
                description="A small yellow {0.names[1].noun} with a long green stem.",
                holder=next(iter(self.lookup["niall"]))
            ).set_state(Engagement.static, Spot.cutthroat_lane),
            Item(
                names=[Name("Teasel"), Name("stem")],
                description="A dry {0.names[1].noun} with a large brown seed head.",
                holder=next(iter(self.lookup["niall"]))
            ).set_state(Engagement.static, Spot.mordiford_quay),
        ]


