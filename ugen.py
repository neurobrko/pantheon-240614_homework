#!/usr/bin/env python

import argparse
import sys
import pandas as pd


# Create custom argument parser to be able to alter error message
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

input_data = []
# load input files into list of lists and strip lines of \n or eventual whitespaces
for file in args.inputFiles:
    for line in file:
        line = line.strip()
        line = line.split(":")
        input_data.append(line)
    file.close()

# create dataframe populated with input_data
column_names = ["ID", "Name", "Middle Name", "Surname", "Department"]
input_df = pd.DataFrame(input_data, columns=column_names)

# create Username column
input_df.insert(
    1,
    "Username",
    input_df["Name"].apply(lambda s: s[0].lower())
    + input_df["Middle Name"].apply(lambda s: s[0].lower() if len(s) > 0 else "")
    + input_df["Surname"].apply(lambda s: s.lower()),
)
# strip Username to 8 characters
input_df["Username"] = input_df["Username"].apply(lambda s: s[:8])
# check for duplicate usernames and add number to them


# custom function to add a number at the end of username
def add_number(username, counts):
    if username in counts:
        counts[username] += 1
        return f"{username}{counts[username]}"
    else:
        counts[username] = 0
        return username


# empty dict for counts for each username
username_counts = {}

# find duplicates and apply the custom function
input_df["is_duplicate"] = input_df.duplicated(subset="Username", keep=False)
input_df["Username"] = input_df.apply(
    lambda x: (
        add_number(x["Username"], username_counts)
        if x["is_duplicate"]
        else x["Username"]
    ),
    axis=1,
)
input_df.drop("is_duplicate", axis=1, inplace=True)

# write input_df to outuput.txt
input_df.to_csv("output_file.txt", header=False, index=False, sep=":")
