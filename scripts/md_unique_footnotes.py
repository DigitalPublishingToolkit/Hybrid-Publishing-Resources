#!/usr/bin/env python

"""
Script turns markdown footnotes from generic to unique, so they wont conflict, when several markdown files are appended onto a single markdown file
In short it appends the name of the file to the footnotes and foonote-references
e.g. "[^22]"  --> "[^1_1-Hart_Keith_22]"
"""

"""
(C) 2015 Andre Castro
License: [GPL3](http://www.gnu.org/copyleft/gpl.html)
"""

import re, sys, os

input_filename=os.path.abspath(sys.argv[1])
input_file = open(input_filename, "r") # open and parse
name = ((os.path.basename(input_filename))[:-3]).encode("ascii")
text = (input_file.read()).decode("utf-8")
fn_regex =  re.compile(r'\[\^(.*?)\]')

def unique_footnoes(text):
#    if bool(re.search(fn_regex, text)) == True:
    sub_text = re.sub(fn_regex, "[^{}_\g<1>]".format(name),text)
    return sub_text.encode("utf-8")
        
sub_text = unique_footnoes(text)
print sub_text
# output_file = open(input_filename, "w") # open and parse
# output_file.write(sub_text)
# output_file.close()
#
