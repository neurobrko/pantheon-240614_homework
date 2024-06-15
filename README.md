# Testing skill + Python for Pantheon.tech

### Part A – pre-requisite
Create a program to generate a list of usernames. The input data is stored in one or more text files with
encoding utf-8. Each line in the input file is a record about one user and includes: ID, forename, middle name
(optional), surname and department. Items in the line are separated by colons.
There is only one output file with all records together. Each line in the output file is a record about one user
and includes: ID, generated username, forename, middle name (optional), surname and department.
You can determine the algorithm used to generate usernames from this example:

#### input_file1.txt

1234:Jozef:Miloslav:Hurban:Legal\
4567:Milan:Rastislav:Stefanik:Defence\
4563:Jozef::Murgas:Development

#### input_file2.txt
1111:Pista::Hufnagel:Sales\
4563:Pista::Hufnagel:Sales

#### input_file3.txt is empty
#### output_file.txt
1234:jmhurban:Jozef:Miloslav:Hurban:Legal\
4567:mrstefan:Milan:Rastislav:Stefanik:Defence\
4563:jmurgas:Jozef::Murgas:Development\
1111:phufnage:Pista::Hufnagel:Sales\
4563:phufnage1:Pista::Hufnagel:Sales

The program is to be launched from the command line these ways:

Displays help:\
python3 ugen.py –h

Processes all input files and writes the generated data to output file:\
python3 ugen.py –o [output file] [input file]...\
It is possible to use also long options, i.e. –-help and --output.\
The help is also displayed if an incorrect input is provided.

### Part B – Unit tests
Create unit tests for the program from the Part A. It is necessary to achieve 100% coverage of relevant code.
The output is an automatically generated report.