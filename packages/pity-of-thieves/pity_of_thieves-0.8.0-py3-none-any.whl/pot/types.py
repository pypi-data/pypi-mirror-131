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


class Engagement(enum.Enum):

    acting = enum.auto()
    hidden = enum.auto()
    player = enum.auto()
    silent = enum.auto()
    static = enum.auto()


class Operation(enum.Enum):

    begins = enum.auto()
    frames = enum.auto()
    paused = enum.auto()
    prompt = enum.auto()
    ending = enum.auto()
    finish = enum.auto()


class Proximity(enum.Enum):

    distant = enum.auto()
    inbound = enum.auto()
    outside = enum.auto()
    outward = enum.auto()
    present = enum.auto()


class Signifier(enum.Enum):

    aelfric = ["Aelfric", "Dene", "Aelfric of Dene"]
    dolphus = ["Dolphus", "Bifling", "Dolphus Bifling"]
    hand = ["fingers", "hand", "stumps"]
    veil = ["mask", "veil"]
