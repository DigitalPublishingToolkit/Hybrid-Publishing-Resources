# INC Hybrid Publication's Resources

This repository consists of a collection of resources aimed at the development hybrid publications, in both reflowable format (EPUB3) and *fixed layout* (Scribus and inDesign structured content).
The resources propose a workflow based on the conversion between markup languages, using [Pandoc]() and [Markdown]() source-files as its essential elements.
Most of the ideas materialized in this collections of resources originated from the research developed by the [Digital Publishing Toolkit]() project, specially the controbutions from [Michael Murtaugh]() and [Silvio Lorusso]().



## Get you git on
To use this repository, clone it by running on the terminal:

`git clone --depth 1 --branch master https://github.com/DigitalPublishingToolkit/Hybrid-Publication-Resources.git DESTINATION_FOLDER`

`cd DESTINATION_FOLDER`

`rm -r .git`


### Add to a remote repository (optional)

Create a new repository inside Github (or anyother online git repository ). Makisure sure **not to** check the `Initialize this repository with a README` option.

And follow the option: **"…or push an existing repository from the command line"** inside the DESTINATION_FOLDER

Alternative you can use the choice **"…or import code from another repository"**


## How to use?
An detailed explanation of how to use this repostory can be found on wiki [wiki/From-Manuscript-to-EPUB](https://github.com/DigitalPublishingToolkit/Hybrid-Publishing-Resources/wiki/From-Manuscript-to-EPUB).



## Guides & Templates
INC guides and templates for essay writing, can be found at
* [wiki/INC styleguide](https://github.com/DigitalPublishingToolkit/Hybrid-Publishing-Resources/wiki/INC-styleguide).
* [wiki/INC template for essays](https://github.com/DigitalPublishingToolkit/Hybrid-Publishing-Resources/wiki/INC-template-essay)




---

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)

The greater part of this framework was developed as part of the [Digital Publishing Toolkit](http://digitalpublishingtoolkit.org) by Michael Murtaught, with the support of Institute for [Network Cultures](http://networkcultures.org)
and [Creating 010](http://creating010.com).

André Castro 2015

---



# TODO
* in `git clone` make depth 1 - no previous history
* rm -tf .git

* font in epub/ ; rm lib/

* integrate `epub_zip.py` and `epub_unzip.py` with `epub_process.py` so that latter does only processing

# Notes from workshop

html5lib missing from macs - fix in epub_process.py

clean up markdown: use pandoc -f markdown -t markdown (see book)

if there is no metadata in markdown md_stripmetada -> dont apply over to the command


