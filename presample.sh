#!/bin/bash
clear
grep fullUrl tweets/scraped.txt | cut -f2- | nl | sed 's/^[ ]*//' > images/presample.txt
