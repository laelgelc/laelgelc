#enter your group number
group=4

#enter the label for your system, mac or linux
mysystem=mac
#mysystem=linux

  if [ "$mysystem" == mac ]
    then
    myshuf=gshuf
    mygsed=gsed
  else
    myshuf=shuf
    mygsed=sed
  fi

presample () {

grep fullUrl tweets/scraped.txt | cut -f2- | nl | sed 's/^[ ]*//' > images/presample.txt

}

getimagesurls () {
    
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

#sort z | uniq > folders
sort z | uniq | sed 's/fl://' > folders
while read folder
do
    mkdir -p images/images/$folder
done < folders

}

grabimages () {

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

}

removedupes () {

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

}

uploadtobucket () {

# google cloud gsutil account = tonyberber@gmail.com

gcloud alpha storage cp -R images/images gs://socialmediaclassimages/group

}

googlelabels () {
    
# speed: 1 file per second

while read folder
do
  mkdir -p images/google_cloud/labels/$folder
  ### rm -f images/google_cloud/labels/$folder/*
done < folders

last=$( tail -1 images/images_index.txt | cut -d'|' -f2 | sed 's/t://'  )

for i in $(eval echo {1..$last});
do
    sed -n "$i"p images/images_index.txt > z
    folder=$( cut -d'|' -f1 z | sed 's/fl://' )
    n=$( cut -d'|' -f2 z | sed 's/t://' )
    id=$( cut -d'|' -f3 z | sed 's/id://' )
    file=$( cut -d'|' -f6 z | sed 's/i://' )
    ext=$( cut -d'|' -f7 z | sed 's/f://' )
    
    echo "---- detect-labels $i / $last ----"
    
    gcloud ml vision detect-labels --max-results=150  gs://socialmediaclassimages/group/"$folder"/"$n"."$ext" > images/google_cloud/labels/"$folder"/"$n".txt
    
done 

}

labeltypes () {
    
rm -f images/labels.txt

last=$( cat images/images_index.txt | wc -l | tr -cd '[0-9]' )

for i in $(eval echo {1..$last});
do    
    sed -n "$i"p images/images_index.txt > z
    folder=$( cut -d'|' -f1 z | sed 's/fl://' )
    n=$( cut -d'|' -f2 z | sed 's/t://' )
    id=$( cut -d'|' -f3 z | sed 's/id://' )
    date=$( cut -d'|' -f4 z | sed 's/d://' )
    username=$( cut -d'|' -f5 z | sed 's/u://' )
    
    echo "---- labeltypes $i / $last ---"
    
    grep  '"description":' images/google_cloud/labels/"$folder"/"$n".txt | cut -d':' -f2 | tr -d '"' | sed -e 's/^[ ]*//' | tr '\n' ' ' | sed 's/, $//' | tr ' ' '_' | sed 's/,_/,/g' | tr -d "'" | tr '[A-Z]' '[a-z]' | sed "s/^/fl:$folder|t:$n|id:$id|d:$date|u:$username|l:/" >> images/labels.txt
    echo >> images/labels.txt
done 

}

toplabels () {

cut -d'|' -f6 images/labels.txt | sed 's/l://' | tr ',' '\n' | sort | uniq -c | sort -nr | sed 's/^[ ]*//' | grep '[a-z]' | head -1000 | cut -d' ' -f2- | nl -nrz | sed 's/^/v/' | tr '\t' ' ' > images/selectedwords

cp images/selectedwords images/var_index.txt

}

sas () {

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

}

datamatrix () {

mkdir -p images/temp

rm -f images/temp/*

cut -d' ' -f1 images/columns | uniq | sort > files

while read n word 
do
  echo "--- $n ---"
  rg -w $n images/columns | sort -t' ' -k1,1 > a
  echo "$n" > images/temp/$n
  join -a 1 -1 1 -2 1 -e 0 files a | sed "s/$/ $n 0/" | cut -d' ' -f3 >> images/temp/$n
done < images/selectedwords

echo "--- images/data.csv ...---"

awk '
        FNR==1 { col++ }
        FNR>max { max=FNR }
        { l[FNR,col]=$0 }
        END {
                for (i=1;i<=max;i++) {
                        for (j=1;j<=col;j++) {
                                printf "%-50s",l[i,j]
                        }
                        print ""
                }
        }
' images/temp/* > u
tr -s ' ' < u | tr ' ' ',' | sed 's/,$//' > images/data.csv

}

correlationmatrix () {

echo "--- python correlation ... ---"

sed 's;data.csv;images/data.csv;' corr.py > p
python3 p > images/correlation

}

formats () {

nlines=$( cat tweets/emoji.txt | wc -l | tr -dc '[0-9]' )

tail +2 images/correlation | tr -s ' ' | sed 's/^/CORR /' > bottom
head -1 images/correlation | tr -s ' ' | sed 's/^[ ]*//' | sed "s/\(v......\)/$nlines/g" | sed 's/^/N . /' > n

sed 's;data.csv;images/data.csv;' std.py > p
python3 p > s 
tr -s ' ' < s | cut -d' ' -f2 | grep -v 'float' | tr '\n' ' ' | sed 's/^/STD	 . /' > std 
echo >> std

sed 's;data.csv;images/data.csv;' mean.py > p
python3 p > m 
tr -s ' ' < m | cut -d' ' -f2 | grep -v 'float' | tr '\n' ' ' | sed 's/^/MEAN . /' > mean
echo >> mean

cat mean std n bottom > images/sas/corr.txt

echo "PROC FORMAT library=work ;
  VALUE  \$lexlabels" > images/sas/word_labels_format.sas
tr '\t' ' ' < images/selectedwords | sed 's/\(.*\) \(.*\)/"\1" = "\2"/' | sed -e 's/&/and/g' -e 's/%/pc/g' >> images/sas/word_labels_format.sas
echo ";
run;
quit;" >> images/sas/word_labels_format.sas

}

examples () {

mkdir -p images/examples
rm -f images/examples/*

html2text -nobs images/sas/output_group"$group"_images/loadtable.html > a

rm -f x??
split -p'=====' a
ls x?? > files

while read file
do
      pole=$( grep '^Factor ' $file | cut -d' ' -f2,3 | sed -e 's/^/f/' -e 's/ //g' )
      sed 's/^[ ]*//' $file | grep '^[0-9]' | tr -dc '[:alpha:][:punct:][0-9]\n ' | sed 's/^/~/' | tr  '[:space:]()' ' ' | tr -s ' ' |  tr '~' '\n' | cut -d' ' -f2 | grep -v '^$' | sed "s/^/$pole /" 
done < files > images/examples/factors


rm -f x??

head -1 images/sas/output_group"$group"_images/group4_images_scores.tsv | tr -d '\r' | tr '\t' '\n' > vars
    
last=$( cut -d' ' -f1 images/examples/factors | tr -dc '[0-9\n]' | sort -nr | head -1 )
    
for i in $(eval echo {1..$last});
do
      column=$( echo " $i + 1 " | bc ) 
      cut -f1,"$column" images/sas/output_group4_images/group4_images_scores_only.tsv  | tail +2 > a

      for pole in pos neg
      do
        echo "--- "f"$i""$pole"" ---" 

        if [ "$pole" == pos ] ; then
           sort -nr -k2,2 a | grep -v '\-' | tr '\t' ' ' | grep -v ' 0' | head -20 | nl -nrz > files
        else
           sort -n -k2,2 a | grep '\-' | tr '\t' ' ' | grep -v ' 0' | grep -v '	0' | head -20 | nl -nrz > files
        fi

        grep f"$i""$pole" images/examples/factors | sort -t' ' -k2,2 | cut -d' ' -f2 | sort > factor_words
        
        while read n file score
        do

          grep -m1 $file images/sas/output_group4_images/group4_images_scores.tsv | tr -d '\r' | tr '\t' '\n' > scores
          paste vars scores | tr '\t' ' ' | grep '^v' | grep -v ' 0$' | cut -d' ' -f1 | sort > vars_text
          join vars_text images/selectedwords | cut -d' ' -f2 | sort > vars_text_codes
          username=$( grep -w $file user_index.txt | cut -d' ' -f2 )
          picture=$( grep -w $file images/images_index.txt | cut -d'|' -f2,7 | tr ':|' ' ' | cut -d' ' -f2,4 | sed 's;\(.*\) \(.*\);\1.\2;' )
          folder=$( grep -w $file images/images_index.txt | cut -d'|' -f1 | tr ':|' ' ' | cut -d' ' -f2  )
          url=$( grep -m1 -B5 $file tweets/jq.txt | grep '"url"'  | cut -d':' -f2- | tr -d '",' | sed 's/^[ ]*//' )
          extension=$( echo $picture | cut -d'.' -f2 )
          cp images/images/$folder/$picture images/examples/image_f"$i""$pole"_x`"$n"."$extension"

          echo "---------------" 

          echo "# $n" 
          echo "score = $score"  
          echo "url: $url"
          echo

          grep -w $file images/labels.txt | tr '|' '\n' | sed 's/l:/~/' | tr '~' '\n'    

          echo
          echo "Lemmas in this picture that loaded on the factor:"
          echo

          join vars_text_codes factor_words > ll
          tr '\n' ',' < ll | sed 's/,/, /g' | sed 's/, $//' > images/examples/lemmas_f"$i"_"$pole"_"$n".txt
          cat ll

          echo 

        done < files > images/examples/examples_f"$i"_"$pole".txt

      done

done

    #rm -f vars factor_words scores vars_text vars_text_codes

}

#presample
#collecturls
#grabimages
#removedupes
#googlelabels
#labeltypes
#toplabels
#sas
#datamatrix
#correlationmatrix
#formats

examples

