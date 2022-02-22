#!/bin/bash

echo "================= CV / pandoc"
pandoc \
       --standalone \
       --include-in-header pandoc/style.css \
       --from markdown --to html \
       --metadata pagetitle="Thomas Guillod / CV" \
       --output data/cv_guillod.html pandoc/resume.md

echo "================= CV / wkhtmltopdf"
wkhtmltopdf -q \
        --zoom 0.9 \
        --page-size A4 \
        --margin-left 5mm \
        --margin-right 5mm \
        --margin-top 10mm \
        --margin-bottom 10mm \
        data/cv_guillod.html data/cv_guillod.pdf
 
 echo "================= CV / exiftool"      
 exiftool -q \
        -overwrite_original \
        -Title="Thomas Guillod / CV" -Author="Thomas Guillod" -Subject="CV / Resume" \
        data/cv_guillod.pdf

 echo "================= SITE / css"      
sass _sass/modern-resume-theme.scss main.css
yui-compressor -o main.css main.css
