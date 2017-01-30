#!/usr/bin/env python

"""
Script that makes YAML file from markdown files - used by audiobook
"""

"""
(C) 2017 Lucia Dossin, PublishingLab

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)

"""

import os

titles = []

if os.path.exists('toc.yaml'):
    print 'File toc.yaml already exists.'
else:
    for i in os.listdir('md'):
        if i.endswith(".md") and not i.endswith('book.md'):

            str1 = "# "; #pandoc parameter used is converting docx to md using atx-headers
            str2 = "\n";
            read = True
            with open('md/'+i, "r") as infile:
                inp = infile.read()
                if read == True:
                    heading = inp.find(str1)
                    lbr = inp[heading:].find(str2)
                    end = heading + lbr
                    title = inp[heading:end].replace('# ','')
                    titles.append(title)
                    read = False

    with open('toc.yaml', 'w') as outfile:
        for r in range(len(titles)):
            print 'chapter'+str(r+1) + ': "'+ titles[r] + '"'
            outfile.write('chapter'+str(r+1) + ': "'+ titles[r] + '"\n')
