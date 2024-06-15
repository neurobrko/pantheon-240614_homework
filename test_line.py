#!/usr/bin/env python
import unittest
from ugen import strip_line, split_line, validate_line


class TestLineProcessing(unittest.TestCase):
    def test_strip_line(self):
        self.assertEqual(
            strip_line("4567:Milan:Rastislav:Stefanik:Defence\n"),
            "4567:Milan:Rastislav:Stefanik:Defence",
        )

    def test_split_line(self):
        self.assertEqual(
            split_line("4567:Milan:Rastislav:Stefanik:Defence"),
            ["4567", "Milan", "Rastislav", "Stefanik", "Defence"],
        )

    def test_validate_line(self):
        self.assertEqual(
            validate_line(
                ["4567", "Milan", "Rastislav", "Stefanik", "Defence"], 1, "", "", ""
            ),
            [["4567", "Milan", "Rastislav", "Stefanik", "Defence"], 1, "", ""],
        )
