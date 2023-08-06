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

import importlib.resources
import functools
import itertools
import random

from balladeer import CommandParser
from balladeer import Drama as DramaType
from balladeer import Grouping
from balladeer import SceneScript
from balladeer.cartography import Compass

from pot.types import Engagement
from pot.types import Operation
from pot.types import Proximity
from pot.world import Map
from pot.world import Character
from pot.world import Mobile


class Drama(DramaType):

    @property
    def ensemble(self):
        transits = {t for c, l, t in self.world.map.options(self.player.spot)}
        return [
            i for i in self.world.lookup.each if isinstance(i, Character)
            or getattr(i, "holder", i).get_state(Map.Spot) == self.player.spot
        ] + list(transits)

    @property
    def folder(self):
        return sorted(importlib.resources.files(self.package).glob("*.rst"))

    @property
    def local(self):
        objects = [
            i for i in self.world.lookup.each
            if i.get_state(Engagement) not in (Engagement.hidden, Engagement.player)
            and getattr(i, "holder", i).get_state(Map.Spot) == self.player.spot
        ]
        return Grouping(list, {k.__name__: v for k, v in self.world.arrange(objects).items()})

    @functools.cached_property
    def player(self):
        return next(
            i for s in self.world.lookup.values() for i in s
            if i.get_state(Engagement) == Engagement.player
        )

    def __init__(self, package, world, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.package = package
        self.world = world

        self.active = self.active.union({
            self.do_again, self.do_look,
            # self.do_go, self.do_hop,
            self.do_hop, self.do_transit,
            self.do_help, self.do_hint, self.do_history,
            self.do_inspect_character, self.do_inspect_item,
            self.do_quit
        })
        self.default_fn = self.do_next

    def if_mobile(self, ensemble=None):
        ensemble = sorted(ensemble or self.ensemble, key=lambda x: x is not self.player)
        assert ensemble[0] is self.player

        for n, i in enumerate(ensemble):
            if isinstance(i, Mobile):
                if i.in_transit and i.get_state(Engagement) != Engagement.static:
                    spot = i.get_state(Map.Spot)
                    route = list(self.world.map.route(spot, i.get_state(Map.Into)))
                    if len(route) > 1:
                        # Still moving
                        i.set_state(route[1])
                        player_spot = self.player.get_state(Map.Spot)
                        if route[0].name == player_spot.name:
                            i.set_state(Proximity.outward)
                        elif len(route) > 2 and route[2].name == player_spot.name:
                            i.set_state(Proximity.inbound)
                        else:
                            i.set_state(Proximity.distant)
                    else:
                        # Arrived
                        i.set_state(Map.Exit[spot.name])

                    yield i

                # Proximity
                player_spot = self.player.get_state(Map.Spot)
                spot = i.get_state(Map.Spot)
                if not spot: continue

                hops = list(self.world.map.route(spot, player_spot))
                if hops[0].name == player_spot.name:
                    i.set_state(Proximity.present)
                elif (
                    len(hops) > 1 and hops[1].name == player_spot.name
                    and i.get_state(Proximity) not in (Proximity.inbound, Proximity.outward)
                ):
                    i.set_state(Proximity.outside)

    def if_patrol(self, ensemble=None):
        ensemble = sorted(ensemble or self.ensemble, key=lambda x: x is not self.player)
        for n, i in enumerate(ensemble):
            if isinstance(i, Mobile) and getattr(i, "patrol", None):
                if not i.in_transit and i.get_state(Engagement) != Engagement.static:
                    i.patrol.rotate()
                    i.set_state(i.patrol[0])
                    yield i

    def interlude(self, folder, index, *args, **kwargs):
        shift = list(self.if_patrol())
        moved = list(self.if_mobile())
        exits = {c: t for c, _, t in self.world.map.options(self.player.spot)}
        return {
            "events": "", # eg: mobile arrives
            "exits": "{0}{1}.".format(
                random.choice(["Exits are: ", "From here you can go "]),
                ", ".join(sorted(
                    ("**{0.name}** via {1.name}" if getattr(v, "names", None) else "**{0.name}**").format(k, v)
                    for k, v in exits.items()
                ))
            )
        }

    def do_again(self, this, text, presenter, *args, **kwargs):
        """
        again | back

        """
        n = len(list(itertools.takewhile(
            lambda x: x.name == this.__name__, self.history
        ))) + 1
        self.state = self.next_states(n)[0]
        return "again..."

    def do_get(self, this, text, presenter, obj: "world.local[Container]", *args, **kwargs):
        """
        get {obj.names[0].noun}
        grab {obj.names[0].noun}
        take {obj.names[0].noun}
        pick up {obj.names[0].noun}

        """
        obj.state = Spot.inventory
        self.active.discard(this)
        return f"{self.world.player.name} picks up {obj.names[0].article.definite} {obj.names[0].noun}.",

    def do_go(self, this, text, presenter, *args, spot: Map.Into, **kwargs):
        """
        go to {spot.value[0]} | go to {spot.value[1]} | go to {spot.value[2]}
        go {spot.value[0]} | go {spot.value[1]} | go {spot.value[2]}
        {spot.value[0]} | {spot.value[1]} | {spot.value[2]}

        """
        self.player.set_state(spot, self.world.map.Exit[self.player.spot.name])
        yield f"Heading to {spot.title}."

    def do_hop(self, this, text, presenter, *args, dirn: Compass, **kwargs):
        """
        {dirn.name}
        go {dirn.name}

        """
        options = {c: l for c, l, t in self.world.map.options(self.player.spot)}
        if dirn not in options:
            return f"There is no {dirn.name} from here."
        else:
            a = Map.Into[options[dirn].name]
            d = self.world.map.Exit[self.player.spot.name]
            self.player.set_state(a, d)
            t = kwargs.pop("transit", None)
            if t:
                return f"Using {t.names[0].article.definite} {t.names[0].noun} to go {dirn.name}."
            else:
                return f"Going {dirn.name}."

    def do_help(self, this, text, presenter, *args, **kwargs):
        """
        help
        what do i do

        """
        self.state = Operation.paused
        options = {
            fn.__name__: list(CommandParser.expand_commands(fn, self.ensemble, parent=self))
            for fn in self.active
        }
        for k, v in sorted(options.items()):
            cmds = []
            for cmd, (fn, kwargs) in v:
                if fn is self.do_go and len(cmd.split()) == 1:
                    continue

                if all(
                    isinstance(i, Map.Spot) or
                    i is self.player or
                    True #i in self.visible.each
                    for i in kwargs.values()
                ):
                    cmds.append(cmd)

            if cmds:
                if k in ("do_propose", "do_counter", "do_confirm", "do_disavow", "do_abandon"):
                    yield from ("* {0}".format(i) for i in cmds if i != str(tuple()))
                else:
                    yield "* {0}".format(random.choice(cmds))

    def do_hint(self, this, text, presenter, *args, **kwargs):
        """
        hint

        """
        return

    def do_history(self, this, text, presenter, *args, **kwargs):
        """
        history

        """
        self.state = Operation.paused
        yield from ("* {0.args[0]}".format(i) for i in self.history if i.args[0])

    def do_inspect_character(self, this, text, presenter, obj: "local[Character]", *args, **kwargs):
        """
        inspect {obj.names[0].noun}

        """
        self.state = Operation.paused
        yield obj.description.format(obj, **self.facts)

        if obj is self.player:
            items = [
                i for i in self.local.each
                if getattr(i, "holder", i).get_state(Map.Spot) == self.player.spot
            ]
            if items:
                yield "\nCarrying:\n"
                yield from ("* {0}".format(i) for i in items)

    def do_inspect_item(self, this, text, presenter, obj: "local[Item]", *args, **kwargs):
        """
        inspect {obj.names[0].noun}

        """
        self.state = Operation.paused
        yield obj.description.format(obj, **self.facts)

    def do_look(self, this, text, presenter, *args, **kwargs):
        """
        look | look around
        where | where am i | where is it

        """
        self.state = Operation.paused
        for i in self.local.each:
            try:
                yield "* {0.names[0].noun}".format(i)
            except (AttributeError, IndexError):
                pass

    def do_next(self, this, text, presenter, *args, **kwargs):
        """
        more | next

        """
        try:
            self.state = self.next_states(0)[1]
        except Exception:
            pass

        return random.choice([
            f"{self.player.name} hesitates.",
            f"{self.player.name} pauses.",
            f"{self.player.name} waits in the {self.player.spot.title} for a moment.",
        ])

    def do_transit(self, this, text, presenter, transit: "world.map.transits", *args, **kwargs):
        """
        follow {transit.names[0].noun} | follow {transit.names[1].noun}
        go {transit.names[0].noun} | go {transit.names[1].noun}
        open {transit.names[0].noun} | open {transit.names[1].noun}
        try {transit.names[0].noun} | try {transit.names[1].noun}
        use {transit.names[0].noun} | use {transit.names[1].noun}

        """
        directions = {t: c for c, l, t in self.world.map.options(self.player.spot)}
        dirn = directions[transit]
        return self.do_hop(self.do_hop, text, presenter, *args, dirn=dirn, transit=transit, **kwargs)

    def do_quit(self, this, text, presenter, *args, **kwargs):
        """
        quit

        """
        self.state = Operation.ending
