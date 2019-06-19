import bibtexparser
import pandas as pd

entrytypes = {
	"article"       : "periodico",
	"conference"    : "conferencia",
	"incollection"  : "caplivro",
	"inproceedings" : "conferencia",
}
entrykeys = {
	"article"       : "journal",
	"conference"    : "booktitle",
	"incollection"  : "booktitle",
	"inproceedings" : "booktitle",
}
search_bases = ["acm", "webofscience", "scopus", "ieeexplore"]
bib_file = "etapa3.bib"
bib_database = None

with open(bib_file) as bibtex_file:
	bib_database = bibtexparser.load(bibtex_file)

dump = {
	"citationkey" : [],
	"title"       : [],
	"authors"     : [],
	"year"        : [],
	"doi"         : [],
	"fromsearch"  : [],
	"worktype"    : [],
	"publishedin" : [],
}

for entry in bib_database.entries:
	citationkey = entry["ID"]
	title = entry["title"].replace("{", "").replace("}", "")
	authors = entry["author"]
	year = entry["year"]
	doi = entry["doi"]
	
	tags = entry["mendeley-tags"].replace("{", "").replace("}", "").replace("\\", "")
	tags = tags.split(",")
	tags = [s for s in tags if any(b in s for b in search_bases)]
	tags = [s.replace("revisao_", "") for s in tags if "revisao_" in s]
	tags.sort()
	fromsearch = ", ".join(tags)
	
	worktype = entrytypes[entry["ENTRYTYPE"]]
	publishedin = entry[entrykeys[entry["ENTRYTYPE"]]]
	
	dump["citationkey"].append(citationkey)
	dump["title"].append(title)
	dump["authors"].append(authors)
	dump["year"].append(year)
	dump["doi"].append(doi)
	dump["fromsearch"].append(fromsearch)
	dump["worktype"].append(worktype)
	dump["publishedin"].append(publishedin)

df = pd.DataFrame(dump)
df = df.astype({"citationkey" : str})
df = df.set_index("citationkey")
df.to_csv("form_dados.csv")

print("DONE!")



