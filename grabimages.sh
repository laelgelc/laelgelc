#!/bin/bash
clear
last=$( cat images/images_index.txt | wc -l | tr -cd '[0-9]' )

for i in $(eval echo {1..$last});
do
    sed -n "$i"p images/images_index.txt > z
    folder=$( cut -d'|' -f1 z | sed 's/fl://' )
    n=$( cut -d'|' -f2 z | sed 's/t://' )
    id=$( cut -d'|' -f3 z | sed 's/id://' )
    file=$( cut -d'|' -f6 z | sed 's/i://' )
    ext=$( cut -d'|' -f7 z | sed 's/f://' )
    
    echo "---- fetching image $n / $last ----"
    
    curl -k "$file" > images/images/"$folder"/"$n"."$ext"
done
