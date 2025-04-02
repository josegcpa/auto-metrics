# to DOI
cat list-of-publications.txt | grep doi | sort | grep -oE 'doi.org/[0-9\.\/a-zA-Z\-]+' > dois.txt

# to pub_names
cat list-of-publications.txt | grep doi | sort | cut -d ')' -f 2-10 | cut -d . -f 1 | sed 's/^ //' > pub_names.txt 