#!/usr/bin/python

"""
Script that makes m4b file (audiobook) from markdown files and toc.yaml

A description of the workflow that inspired this script and that explains each command/step in details can be found on http://www.publishinglab.nl/blog/2016/07/12/craft-your-own-audiobook/
"""

"""
(C) 2017 Lucia Dossin for the PublishingLab

License: [GPL3](http://www.gnu.org/copyleft/gpl.html)

"""

import datetime, os, shutil, subprocess, sys, yaml

p = os.getcwd()

#create-chapters
#deletes existing directories
if os.path.exists(p+'/txt'):
    shutil.rmtree(p+'/txt')
if os.path.exists(p+'/wav'):
    shutil.rmtree( p+'/wav')
if os.path.exists(p+'/mp3'):
    shutil.rmtree( p+'/mp3')
if os.path.exists(p+'/tmp-md'):
    shutil.rmtree( p+'/tmp-md')
if os.path.exists(p+'/txt-ref'):
    shutil.rmtree( p+'/txt-ref')
if os.path.exists(p+'/audiobook'):
    shutil.rmtree( p+'/audiobook')
if os.path.exists(p+'/chapters.mp3'):
    print 'here '
    os.remove(p+'/chapters.mp3')

#makes empty directories to hold txt, wav and mp3 files
os.mkdir( p+'/txt', 0755 )
os.mkdir( p+'/wav', 0755 )
os.mkdir( p+'/mp3', 0755 )
os.mkdir( p+'/tmp-md', 0755);
os.mkdir( p+'/txt-ref', 0755);
os.mkdir( p+'/audiobook', 0755);

#will store chapter duration values
durations = []

#converts all markdown files inside folder "md" into plain text (will be saved inside folder "txt")
for i in os.listdir('md'):
    if i.endswith(".md") :

        print '-.-.-.-.-.-.-.-.-.-.-.-'
        mdfl = os.path.split('md')[1] + '/' + i

        print 'Converting ' + mdfl
        # inliner - converts reference-style Markdown endnotes to Pandoc Markdown's inline footnotes
        # code adapted from https://github.com/ltrgoddard/inliner
        # by Louis Goddard <louisgoddard@gmail.com>

        with open('md/'+i, "r") as input:
            text = input.read()
            #remove * as they do not translate well into speech
            text = text.replace('*','')
            counter = 0

            while True:
                try:
                    counter = counter + 1

                    ref = "[^" + str(counter) + "]:"
                    nextRef = "[^" + str(counter + 1) + "]:"
                    cite = "[^" + str(counter) + "]"

                    refStart = text.index(ref)
                    tLength = len(text)

                    try:
                        refEnd = text.index(nextRef) - 2
                    except ValueError:
                        break
                        # refEnd = -1
                        # refEnd = text.index(tLength) - 2

                    offset = len(str(counter)) + 5
                    note = "^[" + text[refStart+offset:refEnd] + "]"
                    text = text.replace(cite, note)

                except ValueError:
                    refStart = False
                    break

            if refStart == False:
                print("No notes in the document.")
                pass
            else:
                offset = len(str(counter)) + 5

                note = "^[" + text[refStart+offset:len(text)-1] + "]"
                text = text.replace(cite, note)
                text = text.replace("\n    ", " ")
                cutPoint = text.index("\n^")
                text = text[0:cutPoint]
                if counter == 1:
                    print(str(counter) + " note now inline.")
                else:
                    print(str(counter) + " notes now inline.")

            with open('tmp-md/'+i, "w") as output:
                output.write(text)

        #end inliner

        mdf = os.path.split('tmp-md')[1] + '/' + i

        print 'Converting ' + mdf
        txtf =  os.path.split('txt')[1] + '/' +os.path.splitext(i)[0] + ".txt"
        pandoc_args = ['pandoc', '-f', 'markdown-inline_notes', mdf, '-t', 'plain', '-o', txtf]
        try:
            subprocess.check_call(pandoc_args)
            check = True
            print 'Converted ' + mdf + ' into ' + txtf
            print 'Deleting file ' + mdf
            os.remove(mdf)
            print 'Deleted file ' + mdf
            continue
        except:
            check = False
            print 'Error. Please make sure that you have PANDOC installed on your machine.'
            print 'Check http://pandoc.org/installing.html'
            break
    else:
        continue

#removes empty tmp-md folder
print '-.-.-.-.-.-.-.-.-.-.-.-'
print 'Deleting empty "tmp-md" folder'
os.rmdir('tmp-md')

#converts txt files inside folder "txt" into wav (places inside "wav" folder)
if check:
    for i in os.listdir('txt'):
        if i.endswith(".txt") :

            #replace ^ with 'Reference' (more clear and user-friendly to the listener)
            with open('txt/'+i, "r") as input:
                text = input.read()
                text = text.replace('^[',' Reference[')

            with open('txt-ref/'+i, "w") as output:
                output.write(text)

            f = os.path.split('txt-ref')[1] + '/' + i
            forig = os.path.split('txt')[1] + '/' + i

            print '-.-.-.-.-.-.-.-.-.-.-.-'
            print 'Converting ' + f + ' into wav'
            fileout =  os.path.split('wav')[1] + '/' +os.path.splitext(i)[0] + ".wav"
            args = ['flite', '-f', f, '-voice', 'rms', '-o', fileout]
            try:
                subprocess.check_call(args)
                check = True
                # subprocess.check_call(args)
                print 'Converted ' + f + ' into ' + fileout
                print 'Deleting txt files ' + f + ' and ' + forig
                os.remove(f)
                os.remove(forig)
                print 'Deleted files '  + f + ' and ' + forig

                continue
            except:
                check = False
                print 'Error. Please make sure that you have FLITE installed on your machine.'
                print 'Check http://www.festvox.org/flite/download.html and http://www.speech.cs.cmu.edu/flite/doc/flite_4.html'
                break
        else:
            continue

#adds 1sec silence to wav files, converts to mp3, gets and stores durations and delete wav files and folder
if check:
    #removes empty txt folder
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Deleting empty "txt" folder'
    os.rmdir('txt')
    os.rmdir('txt-ref')

    #adds 1s padding to audio files and converts from wav to mp3
    for i in os.listdir('wav'):
        if i.endswith(".wav") :
            wf = os.path.split('wav')[1] + '/' + i
            print 'Adding 1s padding to ' + wf
            finalfile = os.path.split('wav')[1] + '/' +os.path.splitext(i)[0] + "-pad.wav"
            args = ['sox', wf, finalfile, 'pad', '1', '1']
            try:
                subprocess.check_call(args)
                print '-.-.-.-.-.-.-.-.-.-.-.-'
                print 'Added 1s padding into ' + finalfile
                check = True
            except:
                check = False
                print 'Error. Please make sure that you have SOX installed on your machine.'
                print 'Check http://sox.sourceforge.net/'
                break

            #converts wav to mp3
            print '-.-.-.-.-.-.-.-.-.-.-.-'
            print 'Converting ' + finalfile
            mp3f =  os.path.split('mp3')[1] + '/' +os.path.splitext(i)[0] + ".mp3"
            args = ['ffmpeg', '-i', finalfile, '-q:a', '0', mp3f]
            try:
                subprocess.check_call(args)
                print 'Converted ' + finalfile + ' into ' + mp3f

                #gets duration
                #from http://superuser.com/questions/650291/how-to-get-video-duration-in-seconds
                #with thanks to http://trac.ffmpeg.org/wiki/FFprobeTips

                ##FFPROBE is installed with FFMPEG, so no further checking is needed

                args = ['ffprobe', '-of', 'default=noprint_wrappers=1:nokey=1' , '-show_entries', 'format=duration', '-sexagesimal', mp3f]
                d = subprocess.check_output(args)
                durations.append(d.rstrip()) #removes new lines (\n)

                check = True
                print '-.-.-.-.-.-.-.-.-.-.-.-'
                print 'Deleting original wav files ' + wf+ ' and ' + finalfile
                os.remove(wf)
                os.remove(finalfile)
                print 'Deleted files ' + wf + ' and ' + finalfile
                continue
            except:
                check = False
                print 'Error. Please make sure that you have FFMPEG installed on your machine.'
                print 'Check https://ffmpeg.org'
                break

        else:
            continue

if check:
    #removes empty wav folder
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Deleting empty "wav" folder'
    os.rmdir('wav')

    #print the values stored in durations into txt file
    with open('durations.txt', 'w') as outfile:
        subprocess.call(["echo", str(durations)], stdout=outfile)
    #end create-chapters

    #get-durations
    chapStarts = 0

    with open('starts.txt', 'w') as outfile:
        for i in os.listdir('mp3'):
            if i.endswith(".mp3") :
                subprocess.call(["echo", str(datetime.timedelta(seconds=chapStarts))], stdout=outfile)

                #gets duration of mp3 files
                mp3f =  os.path.split('mp3')[1] + '/' +os.path.splitext(i)[0] + ".mp3"
                #outputs durations in seconds (use '-sexagesimal' for formatted output)
                sargs = ['ffprobe', '-of', 'default=noprint_wrappers=1:nokey=1' , '-show_entries', 'format=duration',  mp3f]
                s = subprocess.check_output(sargs)
                chapStarts = chapStarts + int(float(s))
                continue
            else:
                continue
    #end get-durations

#pack-chapters
if check:

    st = "concat:"
    chapNames = []
    chapPrefix = []
    chapTimes = []

    #reads toc.yaml and starts.txt, creates a new file (audiobook.chapters)
    c = open('toc.yaml')
    chapMap = yaml.safe_load(c)
    c.close()

    src = open('starts.txt')
    lines = [line.rstrip('\n') for line in src]
    src.close()

    chapKeys = sorted(chapMap.keys())

    with open('temp.chapters', 'a') as outfile:
        for i in sorted(chapMap.keys()):
            prefix = str(i.upper())
            chapPrefix.append( prefix )
            chapNames.append(str(i.upper() + 'NAME=' + chapMap[i]))
            subprocess.call(["echo", str(i.upper() + 'NAME=' + chapMap[i]) ], stdout=outfile)
            continue

        for i,line in enumerate(lines):
            chapTimes.append(chapPrefix[i] + "=" + lines[i])
            subprocess.call(["echo", chapTimes[i] ], stdout=outfile)
            continue

    #make the chapters file like this:
    # CHAPTER1=00:00:00.000
    # CHAPTER1NAME=Introduction
    # CHAPTER2=00:12:30.000
    # CHAPTER2NAME=Chapter 001
    # CHAPTER3=00:53:20.000
    # CHAPTER3NAME=Chapter 002

    #sort file lines
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Sorting chapters'
    with open('temp.chapters') as f:
        sorted_file = sorted(f)

    #save to a file
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Saving audiobook chapters into file'
    with open('audiobook.chapters', 'w') as f:
        f.writelines(sorted_file)

    os.remove('temp.chapters')

    #concatenates mp3 files into one
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Concatenating mp3 files into one'
    for indx, filename in enumerate(os.listdir('mp3')):
        fullfilename = os.path.split('mp3')[1] + '/' + filename
        st += fullfilename
        if indx < (len(os.listdir('mp3')) - 1):
            st += "|"

    #ffmpeg -i "concat:000.mp3|001.mp3|002.mp3" -q:a 0 chapters.mp3
    #-q:a 0 will ensure higher quality mp3
    args = ['ffmpeg', '-i', st , '-q:a', '0', 'chapters.mp3']
    subprocess.check_call(args)

    #removes duration/start files
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Deleting duration txt files'
    os.remove('durations.txt')
    os.remove('starts.txt')

    #removes mp3 folder and files
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Deleting "mp3" folder and files'
    shutil.rmtree('mp3')

    #adds chapters to audio file
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Adding chapters to audio file'

    #MP4Box -add chapters.mp3 -chap audiobook.chapters audiobook-mp3.mp4
    mpargs = ['MP4Box', '-add', 'chapters.mp3', '-chap', 'audiobook.chapters',  'audiobook-mp3.mp4']
    try:
        subprocess.check_call(mpargs)
        print 'Added chapters to file (mp3 to mp4 conversion)'
        check = True
    except:
        check = False
        print 'Error. Please make sure that you have MP4Box installed on your machine.'
        print 'Check https://gpac.wp.mines-telecom.fr/downloads/'

if check:
    #removes chapters file
    os.remove('audiobook.chapters')
    #removes concatenated mp3 files
    os.remove('chapters.mp3')

    #converts chapters into QT format
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Converting chapters into QT format'

    #mp4chaps --convert --chapter-qt audiobook-mp3.mp4
    chapargs = ['mp4chaps', '--convert', '--chapter-qt', 'audiobook-mp3.mp4']
    try:
        subprocess.check_call(chapargs)
        check = True
    except:
        check = False
        print 'Error. Please make sure that you have mp4chaps installed on your machine.'
        print 'Check https://code.google.com/archive/p/mp4v2/downloads'

if check:
    #adds metadata
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Adding metadata'
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Type the book\'s title: (press <enter> to submit)'
    bookTitle = str(raw_input('Book Title: '))
    print 'Type the author\'s name(s): (press <enter> to submit)'
    bookAuthor = str(raw_input('Book Author: '))
    print 'Type the book\'s publication year: (press <enter> to submit)'
    bookYear = str(raw_input('Book Year: '))

    argTitle='album='+str(bookTitle)
    argAuthor='album_author='+str(bookAuthor)
    argAuthorSingle='author='+str(bookAuthor)
    argYear='year='+str(bookYear)

    #ffmpeg -i audiobook-mp3.mp4 -metadata album_author="Author Name" -metadata album="Book Title" -metadata year="2015" audiobook.final.m4a
    metargs = ['ffmpeg', '-i', 'audiobook-mp3.mp4', '-metadata', argAuthor, '-metadata', argAuthorSingle, '-metadata', argTitle, '-metadata', argYear, 'audiobook-tags.m4a']
    subprocess.check_call(metargs)

    #removes concatenated mp4 file
    os.remove('audiobook-mp3.mp4')

    #renames it to m4b
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Renaming file (m4a -> m4b)'

    #mv audiobook-tags.m4a audiobook.m4b
    args = ['mv', 'audiobook-tags.m4a', 'audiobook/audiobook.m4b']
    subprocess.check_call(args)

    #adds cover pic
    print '-.-.-.-.-.-.-.-.-.-.-.-'
    print 'Add the cover'

    #search for epub/cover.jpg
    if os.path.isfile(p+'/epub/cover.jpg'):
        coverimg = 'epub/cover.jpg'
    else:
        print 'File epub/cover.jpg not found. Type the path to the audiobook\'s cover image. It can be jpg or png and the path is relative to the directory you are in. For example, epub/myimage.png : (press <enter> to submit)'
        #type epub/cover.jpg
        coverimg = str(raw_input('Book Cover: '))

    argCover='cover='+str(coverimg)
    print 'Cover image file: ' + coverimg

    if os.path.isfile(p+'/'+coverimg):
        #MP4Box -itags cover=cover.png audiobook.m4b
        picargs = ['MP4Box', '-itags', argCover, 'audiobook/audiobook.m4b']
        subprocess.check_call(picargs)
    else:
        print 'COVER IMAGE FILE NOT FOUND. Type the path to the audiobook\'s cover image. It can be jpg or png and the path is relative to the directory you are in. For example, epub/myimage.png : (press <enter> to submit)'
        #try again
        coverimg = str(raw_input('Book Cover: '))
        argCover='cover='+str(coverimg)
        print 'Cover image file: ' + coverimg
        if os.path.isfile(p+'/'+coverimg):
            picargs = ['MP4Box', '-itags', argCover, 'audiobook/audiobook.m4b']
            subprocess.check_call(picargs)
        else:
            print 'Cover file image not found. Audiobook will be created anyway.'

    #remove toc.yaml
    #if os.path.isfile(p + '/audiobook/audiobook.m4b'):
    os.remove(p+'/toc.yaml')

#end pack-chapters
