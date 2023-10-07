#!/bin/bash
clear
cut -d'|' -f6 images/labels.txt | sed 's/l://' | tr ',' '\n' | sort | uniq -c | sort -nr | sed 's/^[ ]*//' | grep '[a-z]' | head -1000 | cut -d' ' -f2- | nl -nrz | sed 's/^/v/' | tr '\t' ' ' > images/selectedwords

cp images/selectedwords images/var_index.txt
