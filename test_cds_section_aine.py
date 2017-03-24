def genbank_parser(list, compiler, else_statement = None):
    """
    This function essentially walks through a given directory taking the filenames, sorting by numerical name using
    the numerical_convert() function to convert string filenames into integers.
    It takes the following as parameters:
        list: the list to which the user wishes to append matches
        compiler: the regex compiler in the format re.compile(r"...()...") that the function uses to search for a match group.
        else_statement: this is a string that is appended to the list if no match group is found. It is set to None by default.
    If a match to the regex is found, match group 1 is appended to the list. If not, the else_statement is appended instead.
    Nothing visible is returned, but the list provided will be populated with matches.
    """
    for root, dirs, all_files in os.walk(indir):
        for infile in sorted(all_files, key=numerical_convert):
            open_file = open(os.path.join(root, infile), 'r')
            match = compiler.search(open_file.read())
            if match:
                list.append(str(match.group(1)))
            else:
                list.append(str(else_statement))
    return()

import os
import re
indir = '/Users/ainefairbrother/PycharmProjects/BiocomputingII/genes'

file_name_compiler = re.compile(r'(\d+)')
def numerical_convert(value):
    """
    The main purpose of this function is to take a string containing digits and convert those digits into integers.
    It takes a string as the input. It splits the string into its 'digit' and 'other' components
    Taking every other item (starting with the second one, as the first is '') in the outcome of the split, the string
    format digits are converted to integers using the map() and int() functions.
    The numerical_convert function then returns any digits it found in 'value' in integer format.
    """
    split_value = file_name_compiler.split(value)
    split_value[1::2] = map(int, split_value[1::2])
    return split_value

word = str('CDS')
count = 0
all_cds_no = []
cds_compiler = re.compile(r"^\s{5}CDS")
for root, dirs, all_files in os.walk(indir):
    for infile in sorted(all_files, key=numerical_convert):
        how_many_cds = []
        open_file = open(os.path.join(root, infile), 'r')
        match = cds_compiler.findall(infile)
        print(match)




