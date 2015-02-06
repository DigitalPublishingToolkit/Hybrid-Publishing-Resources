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
	for i in $(alldocx) ; \
	do md=md/`basename $$i .docx`.md ; \
	echo $$md ; \
	pandoc $$i \
	       	--from=docx \
		--to=markdown \
	       	--atx-headers \
	       	-o $$md ; \
	done


book.md: $(allmarkdown)
	for i in $(allmarkdown) ; \
	do ./scripts/md_stripmetada.py $$i >> book.md ; \
	done


ls_md:markdowns $(allmarkdown) # can be become compound rule
	for i in $(allmarkdown) ; \
	do echo $$i; \
	done


# Rule to build the entire book as a single markdown file from the markdown files inside md/





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



clean:  # remove outputs
	rm book.md -f
	rm book.epub -f
	rm *~ */*~ -f #emacs files
# improve rule: rm if file exits
