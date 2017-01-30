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


## Audiobook
Assumes you have valid, well formatted markdown files inside the md folder.

If you would like to convert from docx to md, make sure you use the recipe `make markdownsaudio` instead of `make markdowns`. This is due to the fact that the `make markdowns` recipe runs a script that makes unique footnotes. Not only it is not necessary for the audiobook but also it disturbs the process of moving footnotes from bottom to inline, which is essential to the reading experience in the audiobook.

Make sure there are numbers before the file names according to the order you want - e.g. 00_txt.md, 01_chapter.md, 02_file.md, etc. Also, use atx-style headers (#).

>Markdown offers two styles of headers: Setext and atx. Setext-style headers for h1 and h2 are created by “underlining” with equal signs (=) and hyphens (-), respectively. To create an atx-style header, you put 1-6 hash marks (#) at the beginning of the line — the number of hashes equals the resulting HTML header level.

source: [https://daringfireball.net/projects/markdown/basics](https://daringfireball.net/projects/markdown/basics)

The script will create a metadata file (toc.yaml) and several folders which will be deleted when the process is completed.

During the process, you will be prompted to type some metadata (such as Title and Author) and indicate the file to be used as cover (it can be either jpg or png).

### Usage

`make audiobook`

### Python modules
You will need the following python modules installed:

  * datetime
  * os
  * shutil
  * subprocess
  * sys
  * yaml

To check whether or not you have them installed already, open the Terminal and type

`python -c "import datetime"`

To check another module, type

`python -c "import yaml"`

... and so on. If you don't see any message after running the command, it means that the module is already installed.

If you do need to install any module, first you need to install pip. You can find further info  [here](https://packaging.python.org/installing/#requirements-for-installing-packages).

Sometimes the module you need is in a package and not always they share the same name. In order to find the packages you need to install, a simple online search with the terms 'python install [module name]' should put you in the right track. Once you find it, type in the Terminal:

`pip install [package_name]` without the brackets

For clarification on the terms module and package, check [https://packaging.python.org/glossary/#term-import-package](https://packaging.python.org/glossary/#term-import-package)

### Other requirements
You will also need the software listed below. In the links provided, you will find instructions on how to install them in all operating systems. However, some code samples in the text below might refer exclusively for MacOSX.

To check if the software is installed, in the Terminal type `which pandoc` (replacing pandoc with any other software you might want to check). *If not installed, you will see no response in the terminal.*

#### pandoc (converts md to txt)
Follow the instructions on
[http://pandoc.org/installing.html](http://pandoc.org/installing.html)

#### flite (converts text to speech)
Download it on
[http://www.festvox.org/flite/download.html](http://www.festvox.org/flite/download.html)

To install, follow the instructions on
[http://www.speech.cs.cmu.edu/flite/doc/flite_4.html](http://www.speech.cs.cmu.edu/flite/doc/flite_4.html)

Basically, you should extract the compressed files, then navigate to the folder, type ./configure, make and then make install (you might need to `sudo make install`). Like this (**one line at a time**):

    tar zxvf flite-XXX.tar.gz
    cd flite-XXX
    ./configure
    make
    make install

**Important:** if you get an error in the last step above, you'll need to make a quick fix in a file. Just follow along:

In the flite-2.0.0-release the file was located in the following directory: /flite-2.0.0-release/main/

Navigate to this directory and using Sublime or any other code editor and open the makefile that you find inside. Scroll down and in the last couple of lines, where it reads

    #       The libraries: static and shared (if built)
            cp -pd $(flite_LIBS_deps) $(INSTALLLIBDIR)
    ifdef SHFLAGS
            cp -pd $(SHAREDLIBS) $(VERSIONSHAREDLIBS) $(INSTALLLIBDIR)
    endif

You should write, instead

    #       The libraries: static and shared (if built)
            cp -pR $(flite_LIBS_deps) $(INSTALLLIBDIR)
    ifdef SHFLAGS
            cp -pR $(SHAREDLIBS) $(VERSIONSHAREDLIBS) $(INSTALLLIBDIR)
    endif

You should simply replace the `cp -pd` with `cp -pR` (twice). Save the file. Once this is done, run the last command again.

    make install

If you'd like further explanation on this issue, check [http://stackoverflow.com/questions/23001775/error-installing-flite-on-mac-osx](http://stackoverflow.com/questions/23001775/error-installing-flite-on-mac-osx)

#### sox (adds padding -silence- to wav files)
If you don’t want to compile,
install brew (handy for installing other software as well)
[http://brew.sh/](http://brew.sh/)
Then copy the line you see and paste it in your Terminal

When it’s done, type

`brew install sox`

Alternatively, check
[http://sox.sourceforge.net/Main/Links](http://sox.sourceforge.net/Main/Links)
**(only if you did not install it using brew)**

If you prefer to compile, check
[https://sourceforge.net/projects/sox/files/sox/](https://sourceforge.net/projects/sox/files/sox/)
**(only if you did not install it using brew)**

#### ffmpeg (converts wav to mp3)
You can also install it using brew:

`brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-frei0r --with-libass --with-libvo-aacenc --with-libvorbis --with-libvpx --with-opencore-amr --with-openjpeg --with-opus --with-rtmpdump --with-schroedinger --with-speex --with-theora --with-tools`

This will install ffmpeg and all options available. If errors appear, make sure to read and follow the instructions given on the Terminal.

Alternatively, check [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html ) and after downloading the file, follow the compilation guide:
[https://trac.ffmpeg.org/wiki/CompilationGuide](https://trac.ffmpeg.org/wiki/CompilationGuide)
**(only if you did not install it using brew)**

#### mp4box (wraps mp3 into mp4, adds navigation chapters and metadata, such as the cover)
Navigate to your Desktop or Documents and
`git clone https://github.com/gpac/gpac.git`

In Mac, after git cloning,

    cd gpac
    ./configure
    make
    sudo make install

For other OS's follow the instructions on
[https://gpac.wp.mines-telecom.fr/downloads/](https://gpac.wp.mines-telecom.fr/downloads/)
(scroll down to 'Building GPAC')

#### mp4chaps (converts chapters into QT format)
Download file from
[https://code.google.com/archive/p/mp4v2/downloads](https://code.google.com/archive/p/mp4v2/downloads)

Unzip downloaded file and open INSTALL to read installation instructions - basically the same commands done before (one at a time):

`./configure`

`make`

`make install`

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
