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


# create class for formatting report output
class FormatCli:
    # usage = "test"
    usage = "production"
    match usage:
        case "production":
            GREEN = "\033[92m"
            YELLOW = "\033[93m"
            RED = "\033[91m"
            BOLD = "\033[1m"
            END = "\033[0m"
        case "test":
            GREEN = ""
            YELLOW = ""
            RED = ""
            BOLD = ""
            END = ""


# function to strip lines of \n or eventual whitespace
def strip_line(line):
    line = line.strip()
    return line


# function to split lines into lists
def split_line(line):
    line = line.split(":")
    return line


# function to validate input data
def validate_line(line, i, filename, wrong_format, skipped_lines):
    valid_line = ""
    # check if the separator is correct and there is 5 values in list
    if len(line) != 5:
        wrong_format.append(
            f"{FormatCli.BOLD}{FormatCli.RED}ERR:{FormatCli.END} {filename}, line {i}: Wrong format of data. "
            f"{FormatCli.BOLD}{FormatCli.RED}Line skipped!{FormatCli.END}"
        )
        skipped_lines += 1
        i += 1
    # check if Forename or Surname are not empty
    elif line[1] == "" or line[3] == "":
        wrong_format.append(
            f"{FormatCli.BOLD}{FormatCli.RED}ERR:{FormatCli.END} {filename}, line {i}: "
            f"Forename or Surname is empty. {FormatCli.BOLD}{FormatCli.RED}Line skipped!{FormatCli.END}"
        )
        skipped_lines += 1
        i += 1
    else:
        # check if ID is int
        try:
            int(line[0])
            # all tests passed
            valid_line = line
        except ValueError:
            wrong_format.append(
                f"{FormatCli.BOLD}{FormatCli.RED}ERR:{FormatCli.END} {filename}, line {i}: "
                f"ID is not a number. {FormatCli.BOLD}{FormatCli.RED}Line skipped!{FormatCli.END}"
            )
            skipped_lines += 1
            i += 1

    # check if department is empty
    if len(line) == 5 and line[4] == "":
        wrong_format.append(
            f"{FormatCli.BOLD}{FormatCli.YELLOW}WARN:{FormatCli.END} {filename}, line {i}: "
            f"Department is not specified."
        )

    return [valid_line, i, wrong_format, skipped_lines]


# function to create pandas dataframe
def create_dataframe(input_data):
    column_names = ["ID", "Forename", "Middle Name", "Surname", "Department"]
    input_df = pd.DataFrame(input_data, columns=column_names)
    return input_df


# function to add a number at the end of duplicate username
def add_number(username, counts):
    if username in counts:
        counts[username] += 1
        return f"{username}{counts[username]}"
    else:
        counts[username] = 0
        return username


# function to generate username based on input data
def generate_username(input_df):
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

    # CHECK FOR DUPLICATE USERNAMES AND ADD NUMBER TO THEM
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

    return input_df


# function to get arguments from command line
def get_arguments():
    # Create argument parser
    ap = CustomArgumentParser(
        prog="ugen.py",
        description="Generate list of usernames in single output file based on user info from one or more input files.",
    )
    ap.add_argument(
        "inputFiles",
        help="filename(s) of user info file(s)",
        metavar="INPUT FILE(S)",
        nargs="+",
        type=argparse.FileType("r"),
    )
    ap.add_argument(
        "-o",
        "--output",
        help="specify the name of the output file",
        metavar="OUTPUT FILE",
        type=argparse.FileType("w"),
        required=True,
    )

    # retrieve arguments
    return ap.parse_args()


def main() -> None:
    # DEFINE VARIABLES
    # list for input data
    input_data = []
    # list for wrong formatted lines log
    wrong_format = []
    # create vars for processed lines and skipped lines
    processed_lines = 0
    skipped_lines = 0

    # get arguments
    args = get_arguments()

    # load input files into list of lists
    for file in args.inputFiles:
        i = 1
        for line in file:
            line = strip_line(line)
            # spilt line into list
            line = split_line(line)
            # validate line
            valid_line, i, wrong_format, skipped_lines = validate_line(
                line, i, file.name, wrong_format, skipped_lines
            )
            if valid_line:
                input_data.append(valid_line)
                processed_lines += 1
                i += 1

        file.close()

    # create dataframe populated with input_data
    input_df = create_dataframe(input_data)

    # generate username from existing columns
    input_df = generate_username(input_df)

    # write input_df to output.txt
    input_df.to_csv(args.output, header=False, index=False, sep=":")

    # print report
    print(
        f"{FormatCli.GREEN}{FormatCli.BOLD}{processed_lines} lines processed.{FormatCli.END}"
    )
    if skipped_lines == 0:
        print(f"{FormatCli.BOLD}{skipped_lines} lines skipped.{FormatCli.END}")
    else:
        print(
            f"{FormatCli.RED}{FormatCli.BOLD}{skipped_lines} lines skipped.{FormatCli.END}"
        )
    if wrong_format:
        print(f"\n{FormatCli.RED}{FormatCli.BOLD}ERRORS AND WARNINGS:{FormatCli.END}")
        print(*wrong_format, sep="\n")


if __name__ == "__main__":
    main()
