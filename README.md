# Testing skill + Python for Pantheon.tech

### Part A – pre-requisite
Desired program is called *ugen.py* as required. On top of all the requirements I took the liberty of implementing data validation and printing report after running the script.

I moved the data to separate folder not to mix code and data and to make top folder clearer. Therefor the execution of the script should be:
```
python3 ugen.py -o data/output_file.txt data/input_file1.txt data/input_file2.txt data/input_file3.txt
```
or:
```
python3 ugen.py -o data/output_file.txt data/input_file*
```
**Requirements**\
On top of build-ins only *pandas* package is required for running main script. 

### Part B – Unit tests
To be completely honest I have very, very little previous experience with unit tests. So I have done my fair share of googling, reading documentation, tutorials and StackOverflow. So I hope my *test_ugen.py* meets the goals. As I told your colleague from HR I am willing and happy to learn new skills and up my coding abilities.  

### Part C - Module tests
To continue with my honesty, I have never came across the term Whitebox testing before. So more googling came in. :) I think I grasped some basics of this approach to testing and I hope that produced test report will meet some expectations.

To run the test and writing report:
```
python3 test.py ugen.py test/test_data.txt
```

**Requirements**\
*fpdf2* is needed for running *test.py*. For running the test and generating PDF report. It is also necessary to download *test* directory with *fonts* directory.

### Comments and Hints
**Comments:** To generate documentation directly from code using pydoc would require som refactoring, docstrings and very likely using object-oriented approach to problem. (And some more googling, docs and tutorials on my side.)

**Hints:** I have created three versions.\
*ugen.py* - Main script\
*ugen2.py* - Crude but working version, with data validation implemented\
*ugen3.py* - Basic version, working only in case that input data are 
properly formatted. Otherwise script usually exits with errors, not creating any output.

I have ran *test.py* on all three versions. You can see the results in test reports in *test* folder.

### Conclusioin
I hope you will be content with my work. Apart from some courses on Udemy I am mostly self learned programmer, but I have strong will to learn and a hunger for knowledge. I have a real passion for Python and interest in new technologies. With so many surfacing literally every day I may sometime need a helping hand leading me through them. For example a help from a colleague from Pantheon.

I am looking forward to further communication.

Marek Paulik