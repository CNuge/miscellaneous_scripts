

file_list=$(ls -d *.csv)

for file in $file_list
do
	name=$(echo $file | cut -d '.'  -f 1)
	extension='.tsv'
	new_name=$name$extension
	sed 's:,:\t:g' $file > $new_name
done

