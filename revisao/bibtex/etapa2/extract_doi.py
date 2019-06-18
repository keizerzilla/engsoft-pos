import sys
import bibtexparser

if len(sys.argv) != 2:
	print("uso: python3 extract_doi.py <arquivo-bibtex>")
	sys.exit(1)

bib_database = None
with open(sys.argv[1]) as bibtex_file:
	bib_database = bibtexparser.load(bibtex_file)

if bib_database == None:
	print("erro abrindo arquivo bibtex! abortando...")
	sys.exit(1)

with open(sys.argv[1] + "_doi-list.txt", "w") as doi_list:
	count = 1
	for entry in bib_database.entries:
		try:
			doi_list.write("https://doi.org/" + entry["doi"] + "\n")
		except:
			print("DOI NOT FOUND:", entry["title"])
		
		count = count + 1

