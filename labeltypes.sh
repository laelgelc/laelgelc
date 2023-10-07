#!/bin/bash
clear
rm -f images/labels.txt

last=$( cat images/images_index.txt | wc -l )

for i in $(eval echo {1..$last});
do    
    sed -n "${i}p" images/images_index.txt > z
    folder=$(cut -d'|' -f1 z | sed 's/fl://')
    n=$(cut -d'|' -f2 z | sed 's/t://')
    id=$(cut -d'|' -f3 z | sed 's/id://')
    date=$(cut -d'|' -f4 z | sed 's/d://')
    username=$(cut -d'|' -f5 z | sed 's/u://')

    echo "---- labeltypes $i / $last ---"

# Google Cloud Vision Labels in the format obtained from the original 'googlelabels' function (JSON format)
#    grep '"description":' images/google_cloud/labels/"$folder"/"$n".txt | cut -d':' -f2 | tr -d '"' | sed -e 's/^[ ]*//' | tr '\n' ' ' | tr -d '\r' | sed 's/, $//' | tr ' ' '_' | sed 's/,_/,/g' | tr -d "'" | tr '[A-Z]' '[a-z]' | sed "s/^/fl:$folder|t:$n|id:$id|d:$date|u:$username|l:/" >> images/labels.txt

# Google Cloud Vision Labels in the format obtained from the Python version of the 'googlelabels' function
    grep 'description:' images/google_cloud/labels/"$folder"/"$n".txt | cut -d':' -f2 | tr -d '"' | sed -e 's/^[ ]*//' | tr '\n' ', ' | tr -d '\r' | sed 's/,$//' | tr ' ' '_' | sed 's/,_/,/g' | tr -d "'" | tr '[A-Z]' '[a-z]' | sed "s/^/fl:$folder|t:$n|id:$id|d:$date|u:$username|l:/" >> images/labels.txt
    echo >> images/labels.txt
done
