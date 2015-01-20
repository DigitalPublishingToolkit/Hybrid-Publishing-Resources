# Generic Makefile
#

# markdown sources
sources=$(shell scripts/expand_toc.py --list TOC.md)

clean:
	rm compound_book.md
	rm book.epub



# markdown sources
sources=$(shell scripts/expand_toc.py --list compound/TOC.md)

# Rule to build the entire book as a single markdown file from the table of contents file using expand_toc.py
compound_book.md: compound/TOC.md $(sources)
	scripts/expand_toc.py compound/TOC.md --section-pages --filter scripts/chapter.sh > $@



book.epub: compound_book.md epub/metadata.xml epub/styles.epub.css epub/cover.png
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
		compound_book.md

# # Epub post production - and and enhancements to toolkit.epub
# FromPrintToEbooks.epub: toolkit.epub
# 	python scripts/glossary.py toolkit.epub && \
# 	python scripts/epub_post.py FromPrintToEbooks.epub

# # 

# # needs wkhtmltopdf installed http://wkhtmltopdf.org/
# toolkit.pdf: toolkit.md
# 	cd docs && pandoc --from markdown \
# 	-t html5 \
# 	-s \
# 	--css=styles.pdf.css \
# 	--default-image-extension png \
# 	-o toolkit.html ../toolkit.md && \
# 	wkhtmltopdf --user-style-sheet styles.pdf.css toolkit.html ../toolkit.pdf 



# toolkit.docx: toolkit.md
# 	cd docs && pandoc --default-image-extension png --table-of-contents -o ../toolkit.docx ../toolkit.md

# toolkit.odf: toolkit.md
# 	cd docs && pandoc --default-image-extension png --table-of-contents -o ../toolkit.odf ../toolkit.md


# # Trailer (this rule works for any epub)
# %-trailer.gif: %.epub
# 	python scripts/epubtrailer.py $< --width 320 --height 240 --duration=0.5 -o $@


# toolkit.icml: toolkit.md
# 	cd docs && pandoc \
# 		--from markdown \
# 		--to icml \
# 		--self-contained \
# 		-o ../toolkit.icml \
# 		../toolkit.md
