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

declare -a url=(
    "https://fonts.googleapis.com/css?family=Roboto:100,300,400,700,500,500italic,400italic,300italic,100italic,700italic"
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"
    "https://use.fontawesome.com/releases/v5.11.2/css/all.css"
    "https://use.fontawesome.com/releases/v5.11.2/css/v4-shims.css"
)
                
for i in "${url[@]}"
do
   echo "$(curl -s "$i" | cat - main.css)" > main.css
done

yui-compressor -o main.css  main.css
