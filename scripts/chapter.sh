#!/bin/bash
# Output the title
# the use of html is a hack to prevent the title from being hardwrapped
# (which seems to be the behaviour of pandoc's markdown output mod )
#
# pandoc \
#     --to html  \
#     --template compound/article.head.template.md \
#     $1
#
# now output the rest (as markdown)
pandoc \
    --to markdown \
    --template compound/article.body.template.md \
    --id-prefix=$1- \
    --base-header-level=2 \
    --atx-headers \
    $1
