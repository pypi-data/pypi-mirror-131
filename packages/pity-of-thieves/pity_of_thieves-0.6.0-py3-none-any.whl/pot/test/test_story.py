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

from collections import defaultdict
import string
import unittest

from turberfield.catchphrase.presenter import Presenter
from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript

from pot.story import Story


class Witness(Presenter):

    @classmethod
    def represent(cls, story, *args, facts=None, previous=None, **kwargs):
        rv = story.context.interlude(
            story.context.folder,
            previous and previous.index,
            previous and previous.ensemble
        )
        return cls.build_presenter(
            story.context.folder, *args, facts=facts or rv,
            ensemble=story.context.ensemble + [story.context, story.settings],
            **kwargs
        )

    @staticmethod
    def build_presenter(folder, *args, facts=None, ensemble=None, strict=True, roles=1):
        rv = None
        paths = getattr(folder, "paths", folder)
        pkg = getattr(folder, "pkg", None)
        for n, p in enumerate(paths):
            text = Presenter.load_dialogue(pkg, p)
            text = string.Formatter().vformat(text, args, facts or defaultdict(str))
            rv = Witness.build_from_text(
                text, index=n, ensemble=ensemble or [], strict=strict, roles=roles, path=p
            )
            if rv:
                break

        return rv

    @staticmethod
    def build_from_text(text, index=None, ensemble=[], strict=True, roles=1, path="inline"):
        script = SceneScript(path, doc=SceneScript.read(text))
        selection = script.select(ensemble, roles=roles)
        if all(selection.values()) or (not strict and any(selection.values())):
            script.cast(selection)
            casting = {next(iter(i.attributes.get("names", [])), None): i.persona for i in selection}
            model = script.run()
            rv = Presenter(model, index=index, casting=casting, ensemble=ensemble, text=text)
            for k, v in model.metadata:
                rv.metadata[k].append(v)
            return rv


class StoryTests(unittest.TestCase):

    def setUp(self):
        self.story = Story()

    def test_switch_to_niall(self):
        reply = ""
        for n, cmd in enumerate(["w", "", "", ]):
            with self.subTest(n=n, cmd=cmd):
                presenter = Witness.represent(self.story, reply)
                path = self.story.context.folder[presenter.index]
                if n in (0, 1):
                    self.assertIn("odric", str(path))
                elif n == 2:
                    self.assertIn("niall", str(path))

                animation = next(filter(None, (presenter.animate(f) for f in presenter.frames if f)))
                text = "\n".join(l for l, d in self.story.render_frame_to_terminal(animation))
                reply = self.story.context.deliver(cmd, presenter=presenter)

    def test_errand(self):
        reply = ""
        briony, niall, odric, teasel = [
            next(iter(self.story.context.world.lookup[i])) for i in ("briony", "niall", "odric", "teasel")
        ]
        for n, cmd in enumerate(["w", "", "", "", ""]):
            with self.subTest(n=n, cmd=cmd):
                presenter = Witness.represent(self.story, reply)
                path = self.story.context.folder[presenter.index]
                animation = next(filter(None, (presenter.animate(f) for f in presenter.frames if f)))
                if n in (0, 1):
                    self.assertIn("odric", str(path))
                    self.assertIs(niall, briony.holder)
                elif n == 2:
                    self.assertIn("niall", str(path))
                elif n >= 4:
                    self.assertIn(odric, (briony.holder, teasel.holder))

                text = "\n".join(l for l, d in self.story.render_frame_to_terminal(animation))
                reply = self.story.context.deliver(cmd, presenter=presenter)
