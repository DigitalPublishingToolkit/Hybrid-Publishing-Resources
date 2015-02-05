# Generic Makefile
alldocx=$(wildcard docx/*.docx)
allmarkdown=$(wildcard md/*.md)
markdowns_compound=compound_src.md
epub=book.epub
icmls=$(wildcard icml/*.icml)

test: $(md)
	echo $(addprefix md/, \
	$(notdir \
	$(basename \
	$(wildcard docx/*.docx)))) ; \
	done

markdowns:$(alldocx) # convert docx to md
	for i in $(alldocx); \
	do ./scripts/docx2md.sh $$i; \
	done

example:markdowns $(allmarkdown)
	for i in $(allmarkdown) ; \
	do echo $$i; \
	done

# Explanation rule example
## prereq:
### markdowns (another rule - that creates markdown files) 
### $(allmarkdown) - a var that wildcards all the mardowns in md.
## The prereq#1(rule) is execute and so it can supply the prereq#2(var) with the required files



# CHECK ?? IS TOC.md needed?
# markdown sources
sources=$(shell scripts/expand_toc.py --list TOC.md)

# Rule to build the entire book as a single markdown file from the table of contents file using expand_toc.py
compound_src.md: compound/TOC.md $(sources)
	scripts/expand_toc.py compound/TOC.md --section-pages --filter scripts/chapter.sh > $@



# make docx -> markdown for all docx/*.docx
docx=$(shell script/)










book.epub: compound_src.md epub/metadata.xml epub/styles.epub.css epub/cover.png
	pandoc \
		--from markdown \
		--to epub3 \
		--self-contained \
		--epub-chapter-level=2 \
		--epub-stylesheet=epub/styles.epub.css \
		--epub-cover-image=epub/cover.png \
		--epub-metadata=epub/metadata.xml \
		--epub-embed-font=lib/UbuntuMono-B.ttf \
		--default-image-extension png \
		--toc-depth=2 \
		-o book.epub \
		compound_src.md



clean: # remove outputs
	rm compound_src.md
	rm book.epub
