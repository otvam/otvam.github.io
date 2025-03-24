#!/bin/bash

echo "================= CV / pandoc"
pandoc \
       --standalone \
       --embed-resources \
       --css style.css \
       --from markdown --to html \
       --metadata pagetitle="Thomas Guillod / CV" \
       --output cv_guillod.html resume.md

echo "================= CV / wkhtmltopdf"
wkhtmltopdf -q \
        --zoom 0.9 \
        --page-size letter \
        --margin-left 20mm \
        --margin-right 20mm \
        --margin-top 18mm \
        --margin-bottom 18mm \
        cv_guillod.html cv_guillod.pdf
 
 echo "================= CV / exiftool"      
 exiftool -q \
        -overwrite_original \
        -Title="Thomas Guillod / CV" -Author="Thomas Guillod" -Subject="CV / Resume" \
        cv_guillod.pdf

