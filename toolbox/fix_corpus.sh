mkdir -p fixed/fake_files fixed/true_files

ls fake_files > files
while read file
do
    echo "--- $file ---"
    sed 's/\([0-9]\)\([a-zA-Z]\)/\1 \2/g' fake_files/$file | fold -s > fixed/fake_files/$file
done < files

ls true_files > files
while read file
do
    echo "--- $file ---"
    sed 's/\([0-9]\)\([a-zA-Z]\)/\1 \2/g' true_files/$file | fold -s > fixed/true_files/$file
done < files
