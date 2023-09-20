#!/bin/bash
clear
last=$( cat images/presample.txt | wc -l | tr -dc '[0-9]' )

mkdir -p images

rm -f images/urls.txt  ### WATCH THIS!

for i in $(eval echo {1..$last});
do
        rg -m1 "^"$i"	" images/presample.txt | jq '.' > z
        file=$( grep -m1 'fullUrl' z | cut -d'"' -f4  )
        format=$( echo $file | tr '?&=' '|' | cut -d'|' -f3 )
        id=$( grep -m1 'id"' z | tr '~' ' ' | sed -e 's/^[ ]*//' -e 's/:/~/' | cut -d'~' -f2 | tr -dc '[0-9]' )
        username=$( grep -m1 'username"' z | tr '~' ' ' | sed -e 's/^[ ]*//' -e 's/:/~/' | cut -d'~' -f2 | sed -e 's/"//' -e 's/^[ ]*//' -e 's/",$//' | tr '[:upper:]' '[:lower:]' )
        date=$( grep -m1 'date"' z | tr '~' ' ' | sed -e 's/^[ ]*//' | cut -d'~' -f2 | cut -d'T' -f1 | tr -dc '[0-9-]' )

        echo "---- collecturls $i / $last ----"

        echo "id:"$id"|d:$date|u:"$username"|i:$file|f:$format" >> images/urls.txt
done 

grep 'id:...................|' images/urls.txt | nl -nrz | sed 's/^/t:/' | tr '\t' '|' > w

for n in `seq -w 1 13`  # how many batches
do
  printf "$n\n%.0s" {1..1000}  # how many lines in each batch
done | sed 's/^/fl:/' > z

paste z w | tr '\t' '|' | grep 'id:' > images/images_index.txt

sort z | uniq > folders
while read folder
do
    mkdir -p images/images/$folder
done < folders
