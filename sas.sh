#!/bin/bash
clear
mkdir -p images/sas

rm -f images/columns

cut -d'|' -f3,6 images/labels.txt > a

while read n word 
do
  echo "--- $n ---"
  rg -w $word a | cut -d'|' -f1 | sed -e 's/id://' -e "s/$/ "$n" 1/" >> images/columns 
done < images/selectedwords

sort images/columns | uniq > a ; mv a images/columns  # to avoid words whose accents were stripped to be duplicated in the same text ; SAS can't handle that

#cut -d' ' -f2 tweets/selectedwords | gwc -L 
#head -1 columns | cut -d' ' -f1 | gwc -L

cp images/columns images/sas/data.txt
