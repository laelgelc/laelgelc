#!/bin/bash
clear
# remove duplicate images posted in the same message or in repeated messages by the same user (same message id)
    
cut -d'|' -f3 images/images_index.txt | sed 's/id://' | sort | uniq -c | grep -v ' 1 ' | nl | sed 's/^[ ]*//' | tr '\t' ' ' | tr -s ' ' > d

rm -f remove
while read n maxhits id
do
    echo "--- listing $n ---"
    grep -m$maxhits $id images/images_index.txt | cut -d'|' -f6 | sort | uniq -d | sed 's/i://' > dupes
    
    while read dupe
    do
        grep $dupe images/images_index.txt | tail +2 | cut -d'|' -f2
    done < dupes >> remove
done < d 

# remove duplicate image files
while read dupe
do
    pretty=$( echo $dupe | sed 's/t://' )
    folder=$( grep $dupe images/images_index.txt | cut -d'|' -f1 | sed 's/fl://' )
    ext=$( grep $dupe images/images_index.txt | cut -d'|' -f7 | sed 's/f://' )
    rm -f images/images/"$folder"/"$pretty"."$ext"
    echo "--- removing images/images/"$folder"/"$pretty"."$ext" ---"
done < remove

# remove dupes from index
grep -vf remove images/images_index.txt > z ; mv z images/images_index.txt

# remove dupes from index again, for some reason some still remain
cut -d'|' -f2  images/images_index.txt | cut -d':' -f2 > i
find images/images -type f | cut -d'/' -f4 | cut -d'.' -f1 > f
cat i i f | sort | uniq -c | grep ' 2 ' | cut -c6- | grep -v '^$' | sed 's/^/t:/' > ionly
grep -vf ionly images/images_index.txt > b ; mv b images/images_index.txt

# remove empty image files
find images/images -type f empty -exec rm {} +

# remove empty image files from index
cut -d'|' -f2  images/images_index.txt | cut -d':' -f2 > i
find images/images -type f | cut -d'/' -f4 | cut -d'.' -f1 > f
cat i i f | sort | uniq -c | grep ' 2 ' | cut -c6- | grep -v '^$' | sed 's/^/t:/' > ionly
grep -vf ionly images/images_index.txt > b ; mv b images/images_index.txt
