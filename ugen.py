#!/usr/bin/env python

import argparse
import sys


# Create cusotm argument parser to be able to alter error message
class CustomArgumentParser(argparse.ArgumentParser):
    # redefine error message to print usage along with the error
    def error(self, message):
        sys.stderr.write(f"!!! ERROR !!!\n{message}\n!!! ERROR !!!\n\n")
        self.print_help()
        sys.exit(2)


# Create argument parser
ap = CustomArgumentParser(
    prog="ugen.py",
    description="Generate list of usernames in single output file based on user info from multiple input files.",
)
ap.add_argument(
    "inputFiles",
    help="filename(s) of user info file(s)",
    metavar="FILEPATH",
    nargs="+",
    type=argparse.FileType("r"),
)
ap.add_argument(
    "-o",
    "--output",
    help="Specify the name of the output file.",
    metavar="PATH",
    type=argparse.FileType("w"),
)

# retrieve arguments
args = ap.parse_args()
print(args)
