#!/usr/bin/env python

# Remove YAML metada from markdown files

"""
(C) 2015 Andre Castro

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)

"""

import re, sys, os

input_filename=os.path.abspath(sys.argv[1])
input_file = open(input_filename, "r") # open and parse
text = (input_file.read()).decode("utf-8")
yaml_regex = re.compile(r'(\.\.\.|\-\-\-.*\n(.*\:.*\n){2,}\.\.\.)')

def replace(text):    
    if bool(re.match(yaml_regex, text)) == True:
        sub = re.sub(yaml_regex, '', text)
        print (sub.encode("utf-8"))


replace(text)
