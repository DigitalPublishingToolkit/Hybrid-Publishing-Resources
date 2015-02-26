#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, zipfile, os, shutil, glob, textwrap, re
from os.path import join
from xml.etree import ElementTree as ET
import html5lib
import argparse
"""
(C) 2014 Andre Castro

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)
"""

"""
Script enhances the EPUB created from from Pandoc conversion to EPUB3, namely:

* Removes <sub> from footnotes, since these interferes with the iPad response; relies on CSS instead 
* Replaces back arrows - '↩' - with work 'back'
* makes cover linear inside content.opf <spine>
"""

"""
Note: Script needs Django installed https://code.djangoproject.com/wiki/Distributions
to run urlize def (now commented)


"""

filename = sys.argv[1]
# unzip ePub
fh = open(str(filename), 'rb')
z = zipfile.ZipFile(fh)
for name in z.namelist():
    outpath = "temp"
    z.extract(name, outpath)
fh.close()
temp_dir="temp/"
os.remove(temp_dir+'mimetype') # delete mimetype (will be added later with epub.writestr)

def fn_rm_sup(tree, element): # Removes Footnotes <sub>
    for fn in tree.findall(element):
        for child in list(fn):
            if child.tag == 'sup':                
                number = child.text
                fn.remove(child)
                fn.text=number

def replace_fn_links(tree, element): #replace back arrows with work "back"
    for parag in tree.findall(element):
        anchors = parag.findall("./a")
        for anchor in anchors:
            if '#fn'in anchor.get('href'):
                anchor.text = 'back'

   
def spine(filename): # makes cover & title page linear is <spine>
    tree = ET.parse(filename)
    ET.register_namespace('epub', 'http://www.idpf.org/2007/ops')
    spine = tree.find('.//{http://www.idpf.org/2007/opf}spine')
    manifest = tree.find('.//{http://www.idpf.org/2007/opf}manifest')
    for child in spine.getchildren():
        if child.attrib['idref'] == 'cover_xhtml'or child.attrib['idref'] == 'title_page_xhtml':            
            (child.attrib).pop("linear")
            #child.attrib['linear'] = 'yes'
    return tree


def save_html(content_dir, content_file, tree ):
    doctype = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
    html = ET.tostring(tree,  encoding='utf-8', method='xml')
    html = doctype + html
    xhtml_file = open(content_dir + content_file, "w") 
    xhtml_file.write(html) 
    xhtml_file.close()


temp_ls=os.listdir("temp/")
temp_ls.sort()

            
for f in temp_ls: #loop epub contained files     
    if f[:2]=='ch' and f[-6:]==".xhtml": # all ch*.xhtml        
        filename = "temp/"+f
        xhtml = open(filename, "r") 
        xhtml_parsed = html5lib.parse(xhtml, namespaceHTMLElements=False)
        fn_rm_sup(xhtml_parsed, './/a[@class="footnoteRef"]')
        replace_fn_links(xhtml_parsed, './/section[@class="footnotes"]/ol/li/p')        
        
        save_html(
            content_dir=temp_dir,
            content_file=f,
            tree=xhtml_parsed )
        
    elif f == 'content.opf': # the opf
        filename = "temp/"+f
        xhtml = open("temp/"+f, "r")
        tree = spine(filename)
        ET.register_namespace('', 'http://www.idpf.org/2007/opf')
        tree.write(filename, encoding='utf-8', xml_declaration='True' )
        
# Step 3: zip epub
epub = zipfile.ZipFile("book.epub", "w")
epub.writestr("mimetype", "application/epub+zip")
temp_dir = "temp"

def fileList(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches

dirlist=fileList(temp_dir)

for name in dirlist:
    path = name[5:] # removes 'temp/'
    epub.write(name, path, zipfile.ZIP_DEFLATED)

    
epub.close()

# Step 4: clean up: rm temp zipname
shutil.rmtree(temp_dir)

print
print "** EPUB (processed) was generated without errors **"

