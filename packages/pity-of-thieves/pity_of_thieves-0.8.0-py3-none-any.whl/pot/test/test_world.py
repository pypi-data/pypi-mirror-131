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

import unittest

from balladeer import Stateful

from pot.world import Map
from pot.world import World


class MapTests(unittest.TestCase):

    def setUp(self):
        self.map = Map()

    def test_spots(self):
        self.assertEqual(21, len(self.map.Spot))

    def test_vias(self):
        self.assertEqual(21, len(self.map.Spot))

    def test_transits(self):
        transits = [t for c, l, t in self.map.options(self.map.Spot.north_gate)]
        self.assertIn("woodland path", [i.lower() for t in transits for i in str(t).splitlines()])

    def test_routes_lhs(self):
        dep = self.map.exit.mordiford_quay
        arr = self.map.into.beggars_ash
        rv = self.map.route(dep, arr)
        self.assertEqual(7, len(rv), rv)
        self.assertIn("north gate", [v for i in rv for v in i.value])

    def test_routes_rhs(self):
        dep = self.map.exit.tower_street_w
        arr = self.map.into.gardens
        rv = self.map.route(dep, arr)
        self.assertEqual(4, len(rv), rv)
        self.assertIn("upper tower street", [v for i in rv for v in i.value])


class WorldTests(unittest.TestCase):

    def setUp(self):
        self.world = World(Map())

    def test_build(self):
        self.assertTrue(list(self.world.lookup.keys()))

    def test_locations(self):
        self.assertIn("tower st", self.world.lookup)

    def test_ownership(self):
        knife = next(iter(self.world.lookup["knife"]))
        orchard = next(iter(self.world.lookup["orchard"]))
        self.assertIs(orchard, knife.holder)
        self.assertEqual(Map.Spot.orchard, knife.get_state(Map.Spot))
