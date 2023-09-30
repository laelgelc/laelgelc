#!/bin/bash
clear
mkdir -p images

grep fullUrl tweets/scraped.txt | cut -f2- | nl | sed 's/^[ ]*//' > images/presample.txt
