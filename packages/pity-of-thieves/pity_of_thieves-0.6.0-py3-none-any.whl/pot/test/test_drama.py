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

import timeit
import unittest

from balladeer.speech import Name

from turberfield.catchphrase.parser import CommandParser

from pot.drama import Drama
from pot.types import Engagement
from pot.types import Proximity
from pot.world import Character
from pot.world import Spot
from pot.world import Map
from pot.world import Mobile
from pot.world import World


class DramaTests(unittest.TestCase):

    class TestWorld(World):

        def build(self):
            return [Character(names=[Name("test")]).set_state(Engagement.player, Spot.woodshed)]

    def setUp(self):
        world = World(Map())
        self.assertTrue(world.map)
        self.drama = Drama("pot.dlg.odric", world)

    def test_spots(self):
        self.assertEqual(3, len(self.drama.folder), self.drama.folder)

    def test_ensemble(self):
        gerod = next(iter(self.drama.world.lookup["gerod"])).set_state(Engagement.acting)

        self.assertIn(gerod, self.drama.ensemble)
        self.assertIn(self.drama.player, self.drama.ensemble)

        gerod.set_state(Spot.woodshed)
        self.assertIn(gerod, self.drama.ensemble)

    def test_local(self):
        iysla = next(iter(self.drama.world.lookup["iysla"])).set_state(Engagement.acting)
        poison = next(iter(self.drama.world.lookup["poison"])).set_state(Engagement.acting)
        self.assertNotIn(self.drama.player, self.drama.local["Character"])
        self.assertIn(iysla, self.drama.local["Character"])
        self.assertIn(poison, self.drama.local["Item"])

    def test_location(self):
        player = next(iter(self.drama.world.lookup["odric"]))
        player.set_state(self.drama.world.map.Spot.mordiford_quay)
        local = next(iter(self.drama.world.lookup["quay"]))
        self.assertIn(local, self.drama.ensemble)

    def test_if_mobile_proximity(self):
        Spot = self.drama.world.map.Spot
        player = next(iter(self.drama.world.lookup["odric"])).set_state(Spot.yard)
        iysla = next(iter(self.drama.world.lookup["iysla"])).set_state(Spot.yard)
        niall = next(iter(self.drama.world.lookup["niall"]))
        moves = []
        for n in range(5):
            with self.subTest(n=n):
                if n:
                    self.assertEqual(Proximity.present, iysla.get_state(Proximity))
                if n == 0:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.south_end, niall.get_state(Spot))
                elif n == 1:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(1, len(moves))
                    self.assertIs(niall, moves[0])
                    self.assertEqual(Spot.top_cross, niall.get_state(Spot))
                elif n == 2:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(1, len(moves))
                    self.assertIs(niall, moves[0])
                    self.assertEqual(Spot.butchers_row, niall.get_state(Spot))
                    self.assertEqual(Proximity.inbound, niall.get_state(Proximity))
                elif n == 3:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(1, len(moves))
                    self.assertIs(niall, moves[0])
                    self.assertEqual(Spot.yard, niall.get_state(Spot))
                    self.assertEqual(Proximity.present, niall.get_state(Proximity))
                elif n == 4:
                    self.assertFalse(niall.in_transit)
                    self.assertEqual(1, len(moves))
                    self.assertEqual(Spot.north_gate, niall.get_state(Spot))
                    self.assertEqual(Proximity.outward, niall.get_state(Proximity))

                moves = list(self.drama.if_mobile(self.drama.ensemble))

    def test_if_mobile_patrolling(self):
        Spot = self.drama.world.map.Spot
        player = next(iter(self.drama.world.lookup["odric"])).set_state(Spot.yard)
        niall = next(iter(self.drama.world.lookup["niall"]))
        moves = []
        for n in range(16):
            with self.subTest(n=n):
                if n == 0:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.south_end, niall.get_state(Spot))
                elif n == 1:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.top_cross, niall.get_state(Spot))
                elif n == 2:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.butchers_row, niall.get_state(Spot))
                elif n == 3:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.yard, niall.get_state(Spot))
                elif n == 4:
                    self.assertFalse(niall.in_transit)
                    self.assertEqual(Spot.north_gate, niall.get_state(Spot))
                elif n == 5:
                    self.assertFalse(niall.in_transit)
                    self.assertEqual(Spot.north_gate, niall.get_state(Spot))
                elif n == 6:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.yard, niall.get_state(Spot))
                elif n == 7:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.butchers_row, niall.get_state(Spot))
                elif n == 12:
                    self.assertTrue(niall.in_transit)
                    self.assertEqual(Spot.yard, niall.get_state(Spot))

                shift = list(self.drama.if_patrol(self.drama.ensemble))
                moves = list(self.drama.if_mobile(self.drama.ensemble))

    def test_if_mobile_routing(self):
        player = next(iter(self.drama.world.lookup["odric"]))
        self.assertIsInstance(player, Mobile)
        player.set_state(
            self.drama.world.map.Exit.mordiford_quay,
            self.drama.world.map.Spot.mordiford_quay,
            self.drama.world.map.Into.cutthroat_lane,
        )
        Spot = self.drama.world.map.Spot
        for n in range(7):
            moves = list(self.drama.if_mobile(self.drama.ensemble))
            with self.subTest(n=n):
                if n == 5:
                    self.assertIs(player, moves[0])
                    self.assertEqual(
                        Spot.cutthroat_lane,
                        player.get_state(Spot)
                    )
                elif n == 6:
                    self.assertFalse(moves)
                    self.assertEqual(
                        Spot.cutthroat_lane,
                        player.get_state(Spot)
                    )
                else:
                    self.assertIs(player, moves[0])
                    self.assertNotEqual(
                        Spot.cutthroat_lane,
                        player.get_state(Spot)
                    )

    def test_routing_penalty(self):
        timer = timeit.Timer(
            'list(Drama("pot.dlg.odric", World(Map())).if_mobile())',
            setup="from pot.drama import Drama; from pot.world import Map, World"
        )
        t = timer.timeit(6)
        self.assertLess(t, 1.0)

    def test_interlude(self):
        facts = self.drama.interlude(self.drama.folder, 0)
        self.assertIsInstance(facts, dict)
        self.assertIn("exits", facts)
        self.assertIn("**W**", facts["exits"], facts)
        self.assertIn("door", facts["exits"].lower(), facts)

    def test_hop(self):
        Into = self.drama.world.map.Into
        Spot = self.drama.world.map.Spot
        Exit = self.drama.world.map.Exit

        self.assertEqual(Spot.woodshed, self.drama.player.get_state(Spot))
        rv = CommandParser.expand_commands(self.drama.do_hop, ensemble=self.drama.ensemble, parent=self.drama)
        commands = {i[0] for i in rv}
        self.assertIn("n", commands)
        self.assertIn("go n", commands)
        self.assertIn("w", commands)
        self.assertIn("go w", commands)

        fn, args, kwargs = self.drama.interpret(self.drama.match("w"))
        self.assertEqual(self.drama.do_hop, fn)

        fn, args, kwargs =self.drama.interpret(self.drama.match("go w"))
        self.assertEqual(self.drama.do_hop, fn)

        response = self.drama(fn, *args, **kwargs)
        self.assertIn("W", response)
        self.assertEqual(Exit.woodshed, self.drama.player.get_state(Exit))
        self.assertEqual(Into.yard, self.drama.player.get_state(Into))

    def test_go(self):
        Into = self.drama.world.map.Into
        Spot = self.drama.world.map.Spot
        Exit = self.drama.world.map.Exit

        self.assertEqual(Spot.woodshed, self.drama.player.get_state(Spot))
        rv = CommandParser.expand_commands(self.drama.do_go, ensemble=self.drama.ensemble, parent=self.drama)
        commands = {i[0] for i in rv}
        self.assertIn("butchers row", commands)
        self.assertIn("go butchers row", commands)
        self.assertIn("cutthroat lane", commands)
        self.assertIn("go cutthroat lane", commands)

        self.assertNotIn(self.drama.do_go, self.drama.active)
        self.drama.active.add(self.drama.do_go)
        fn, args, kwargs = self.drama.interpret(self.drama.match("butchers row"))
        self.assertEqual(self.drama.do_go, fn)

        fn, args, kwargs =self.drama.interpret(self.drama.match("go butchers row"))
        self.assertEqual(self.drama.do_go, fn)

        response = self.drama(fn, *args, **kwargs)
        self.assertIn("Butchers' Row", response)
        self.assertEqual(Exit.woodshed, self.drama.player.get_state(Exit))
        self.assertEqual(Into.butchers_row, self.drama.player.get_state(Into))

    def test_transit(self):
        Into = self.drama.world.map.Into
        Spot = self.drama.world.map.Spot
        Exit = self.drama.world.map.Exit

        self.assertEqual(Spot.woodshed, self.drama.player.get_state(Spot))
        rv = CommandParser.expand_commands(self.drama.do_transit, ensemble=self.drama.ensemble, parent=self.drama)
        commands = {i[0] for i in rv}
        self.assertIn("open door", commands, self.drama.ensemble)
        self.assertIn("try shed door", commands)

        fn, args, kwargs = self.drama.interpret(self.drama.match("open door"))
        self.assertEqual(self.drama.do_transit, fn)

        fn, args, kwargs =self.drama.interpret(self.drama.match("try shed door"))
        self.assertEqual(self.drama.do_transit, fn)

        response = self.drama(fn, *args, **kwargs)
        self.assertIn("W", response)
        self.assertEqual(Exit.woodshed, self.drama.player.get_state(Exit))
        self.assertEqual(Into.yard, self.drama.player.get_state(Into))
