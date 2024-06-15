#!/usr/bin/env python
import unittest
import pandas as pd
from ugen import (
    strip_line,
    split_line,
    validate_line,
    create_dataframe,
    generate_username,
)


class TestLineProcessing(unittest.TestCase):
    def test_strip_line(self):
        """Strip line of \\n and whitespaces"""
        self.assertEqual(
            strip_line("4567:Milan:Rastislav:Stefanik:Defence\n"),
            "4567:Milan:Rastislav:Stefanik:Defence",
        )

    def test_split_line(self):
        """Split line into list"""
        self.assertEqual(
            split_line("4567:Milan:Rastislav:Stefanik:Defence"),
            ["4567", "Milan", "Rastislav", "Stefanik", "Defence"],
        )

    def test_validate_line(self):
        """Validate values in list from line"""
        self.assertEqual(
            validate_line(
                ["4567", "Milan", "Rastislav", "Stefanik", "Defence"], 1, "", "", ""
            ),
            [["4567", "Milan", "Rastislav", "Stefanik", "Defence"], 1, "", ""],
        )

    def test_create_dataframe(self):
        """Create dataframe from list of lists"""
        input_data = [
            ["1234", "Jozef", "Miloslav", "Hurban", "Legal"],
            ["4567", "Milan", "Rastislav", "Stefanik", "Defence"],
            ["4563", "Jozef", "", "Murgas", "Development"],
            ["1111", "Pista", "", "Hufnagel", "Sales"],
            ["4563", "Pista", "", "Hufnagel", "Sales"],
        ]
        test_df = pd.DataFrame(
            {
                "ID": ["1234", "4567", "4563", "1111", "4563"],
                "Forename": ["Jozef", "Milan", "Jozef", "Pista", "Pista"],
                "Middle Name": ["Miloslav", "Rastislav", "", "", ""],
                "Surname": ["Hurban", "Stefanik", "Murgas", "Hufnagel", "Hufnagel"],
                "Department": ["Legal", "Defence", "Development", "Sales", "Sales"],
            }
        )
        pd.testing.assert_frame_equal(create_dataframe(input_data), test_df)

    def test_generate_username(self):
        """Generate valid username from existing columns"""
        input_df = pd.DataFrame(
            {
                "ID": ["1234", "4567", "4563", "1111", "4563"],
                "Forename": ["Jozef", "Milan", "Jozef", "Pista", "Pista"],
                "Middle Name": ["Miloslav", "Rastislav", "", "", ""],
                "Surname": ["Hurban", "Stefanik", "Murgas", "Hufnagel", "Hufnagel"],
                "Department": ["Legal", "Defence", "Development", "Sales", "Sales"],
            }
        )
        test_df = pd.DataFrame(
            {
                "ID": ["1234", "4567", "4563", "1111", "4563"],
                "Username": [
                    "jmhurban",
                    "mrstefan",
                    "jmurgas",
                    "phufnage",
                    "phufnage1",
                ],
                "Forename": ["Jozef", "Milan", "Jozef", "Pista", "Pista"],
                "Middle Name": ["Miloslav", "Rastislav", "", "", ""],
                "Surname": ["Hurban", "Stefanik", "Murgas", "Hufnagel", "Hufnagel"],
                "Department": ["Legal", "Defence", "Development", "Sales", "Sales"],
            }
        )
        pd.testing.assert_frame_equal(generate_username(input_df), test_df)


if __name__ == "__main__":
    unittest.main(verbosity=2)
