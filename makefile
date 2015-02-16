# Generic Makefile
alldocx=$(wildcard docx/*.docx)
allmarkdown=$(filter-out md/book.md, $(shell ls md/*.md))
markdowns_compound=compound_src.md
epub=book.epub
icmls=$(wildcard icml/*.icml)

test: $(allmarkdown)
	echo "start" ; 
	echo $(allmarkdown) ; 
	echo "end" ;

	# echo $(addprefix md/, \
	# $(notdir \
	# $(basename \
	# $(wildcard docx/*.docx)))) ; \

markdowns:$(alldocx) # convert docx to md
	for i in $(alldocx) ; \
	do md=md/`basename $$i .docx`.md ; \
	pandoc $$i \
	       	--from=docx \
		--to=markdown \
	       	--atx-headers \
		--template=essay.md.template \
		-o $$md ; \
	./scripts/md_unique_footnotes.py $$md ; \
	done



icmls: $(allmarkdown)
	for i in $(allmarkdown) ; \
	do icml=icml/`basename $$i .md`.icml ; \
	./scripts/md_stripmetada.py $$i > md/tmp.md ; \
	pandoc md/tmp.md \
		--from=markdown \
		--to=icml \
		--self-contained \
		-o $$icml ; \
	done



book.md: clean $(allmarkdown)
	for i in $(allmarkdown) ; \
	do ./scripts/md_stripmetada.py $$i >> md/book.md ; \
	done



book.epub: clean book.md epub/metadata.xml epub/styles.epub.css epub/cover.png
	pandoc \
		--from markdown \
		--to epub3 \
		--self-contained \
		--epub-chapter-level=1 \
		--epub-stylesheet=epub/styles.epub.css \
		--epub-cover-image=epub/cover.png \
		--epub-metadata=epub/metadata.xml \
		--default-image-extension png \
		--toc-depth=1 \
		-o book.epub \
		md/book.md ;
	python scripts/epub_process.py book.epub ;

#		--epub-embed-font=lib/UbuntuMono-B.ttf \

clean:  # remove outputs
	rm md/book.md -f
	rm book.epub -f
	rm *~ */*~ -f #emacs files
# improve rule: rm if file exits
