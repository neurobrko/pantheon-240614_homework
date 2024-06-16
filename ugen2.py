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

# create list for input data
input_data = []
# create list for wrong formatted lines
wrong_format = []
# create vars for processed lines and skipped lines
processed_lines = 0
skipped_lines = 0

# load input files into list of lists
for file in args.inputFiles:
    i = 1
    for line in file:
        # strip lines of \n or eventual whitespaces
        line = line.strip()
        # spilt line into list
        line = line.split(":")

        # check if the separator was correct and there is 5 values in list
        if len(line) != 5:
            wrong_format.append(
                f"ERR: {file.name}, line {i}: Wrong format of data. " f"Line skipped!"
            )
            skipped_lines += 1
            i += 1
            continue

        # check if ID is int
        try:
            int(line[0])
        except ValueError:
            wrong_format.append(
                f"ERR: {file.name}, line {i}: " f"ID is not a number. Line skipped!"
            )
            skipped_lines += 1
            i += 1
            continue

        # check if Forename or Surname are not empty
        if line[1] == "" or line[3] == "":
            wrong_format.append(
                f"ERR: {file.name}, line {i}: "
                f"Forename or Surname is empty. Line skipped!"
            )
            skipped_lines += 1
            i += 1
            continue

        # check if department is empty
        if line[4] == "":
            wrong_format.append(
                f"WARN: {file.name}, line {i}: " f"Department is not specified."
            )

        input_data.append(line)
        processed_lines += 1
        i += 1

    file.close()

# create dataframe populated with input_data
column_names = ["ID", "Forename", "Middle Name", "Surname", "Department"]
input_df = pd.DataFrame(input_data, columns=column_names)

# create Username column
input_df.insert(
    1,
    "Username",
    input_df["Forename"].apply(lambda s: s[0].lower())
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
input_df.to_csv(args.output, header=False, index=False, sep=":")

# print report
print(f"{processed_lines} lines processed.")
if skipped_lines == 0:
    print(f"{skipped_lines} lines skipped.")
else:
    print(f"{skipped_lines} lines skipped.")
if wrong_format:
    print(f"\nERRORS AND WARNINGS:")
    print(*wrong_format, sep="\n")
