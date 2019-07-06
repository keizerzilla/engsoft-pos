import re
import sys
import seaborn
import bibtexparser
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def form_base_extraction(bib_file):
	entrytypes = {
		"article"       : "periodico",
		"conference"    : "conferencia",
		"incollection"  : "periodico",
		"inproceedings" : "conferencia",
	}
	entrykeys = {
		"article"       : "journal",
		"conference"    : "booktitle",
		"incollection"  : "booktitle",
		"inproceedings" : "booktitle",
	}
	search_bases = ["acm", "webofscience", "scopus", "ieeexplore"]
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
		
		try:
			authors = entry["author"]
		except:
			#print("authors error:", entry["title"])
			pass
		
		year = entry["year"]
		
		try:
			doi = entry["doi"]
		except:
			#print("doi error:", entry["title"])
			pass
		
		try:
			tags = entry["mendeley-tags"].replace("{", "").replace("}", "").replace("\\", "")
			tags = tags.split(",")
			tags = [s for s in tags if any(b in s for b in search_bases)]
			tags = [s.replace("revisao_", "") for s in tags if "revisao_" in s]
			tags.sort()
			fromsearch = ", ".join(tags)
		except:
			#print("tag error:", entry["title"])
			pass
		
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
	#df.to_csv("form_dados.csv")

	print(bib_file, "done!")
	
	return df

def analysis_time():
	search_engines = {
		"webofscience" : [],
		"scopus" : [],
		"ieeexplore" : [],
		"acm" : [],
	}
	
	worktypes = {
		"conferencia" : [],
		"periodico" : [],
	}
	
	years = {
		"2015" : [],
		"2016" : [],
		"2017" : [],
		"2018" : [],
		"2019" : [],
	}
	
	etapas = ["etapa1/etapa1.bib",
	          "etapa2/etapa2.bib",
	          "etapa3/etapa3.bib",
	          "etapa4/etapa4.bib"]
	
	for etapa in etapas:
		df = form_base_extraction(etapa)
		
		fromsearch = df["fromsearch"].tolist()
		dump = []
		for x in fromsearch:
			for y in re.split('; |, ', x):
				dump.append(y)
		
		unique_fromsearch = Counter(dump)
		for key, value in unique_fromsearch.items():
			search_engines[key].append(value)
		
		worktype = df["worktype"].value_counts()
		for key, value in worktype.items():
			worktypes[key].append(value)
		
		year = df["year"].value_counts()
		for key, value in year.items():
			years[key].append(value)
	
	print(search_engines)
	print(worktypes)
	print(years)
	
	search_engines = pd.DataFrame(search_engines)
	worktypes = pd.DataFrame(worktypes)
	years = pd.DataFrame(years)

def etapa4_analysis():
	seaborn.set()
	df = form_base_extraction("etapa4/etapa4_update.bib")
	
	# trabalhos por ano
	year = df["year"].value_counts()
	year = year.reindex(index=["2015", "2016", "2017", "2018", "2019"])
	print(year)
	ax = year.plot.bar(rot=0)
	
	for i in ax.patches:
		ax.text(i.get_x(), i.get_height(), str((i.get_height())), fontsize=10)

	plt.title("Número de trabalhos por ano de publicação")
	plt.savefig("fig_trabalhos_por_ano.png")
	plt.close()
	
	# trabalhos por searchengine
	fromsearch = df["fromsearch"].tolist()
	dump = []
	for x in fromsearch:
		for y in re.split('; |, ', x):
			dump.append(y)
	
	fromsearch = {"engine" : dump}
	fromsearch = pd.DataFrame(fromsearch)
	unique = fromsearch["engine"].value_counts()
	total = unique.sum()
	ax = unique.plot.bar(rot=0)
	
	for i in ax.patches:
		value = str(round((i.get_height()/total)*100, 2)) + "%"
		ax.text(i.get_x(), i.get_height(), value, fontsize=10)
	
	plt.title("Influência global das fontes de busca")
	plt.savefig("fig_influencia_global_fontes.png")
	plt.close()
	
	# tipos de trabalho
	worktype = df["worktype"].value_counts()
	ax = worktype.plot.bar(rot=0)
	
	for i in ax.patches:
		ax.text(i.get_x(), i.get_height(), str((i.get_height())), fontsize=10)
	
	plt.title("Número de trabalhos por tipo de publicação")
	plt.savefig("fig_trabalhos_por_publicacao.png")
	plt.close()
	
	# veiculos mais usados
	publi = df["publishedin"].tolist()

def barh(column, title="ASDF"):
	seaborn.set()
	df = pd.read_csv("prototipo/revisao_ES2019_formulario_dados.csv", sep="|")
	
	prep = df[column].tolist()
	
	dump = []
	for p in prep:
		for x in p.split(";"):
			dump.append(x.strip())
	
	prep = pd.DataFrame({column : dump})
	prep = prep[column].value_counts().sort_values()
	
	print(prep)
	
	ax = prep.plot.barh(rot=0, color="red")
	
	for i in ax.patches:
		ax.text(i.get_width(), i.get_y(), str(i.get_width()), fontsize=10)
	
	plt.title(title)
	plt.tight_layout()
	plt.show()

def research_questions():
	# bases de dados
	#barh("DATABASES")
	
	# preprocessamentos
	#barh("PREPROCESSINGS", "Etapas de pré-processamento")
	
	# atributos
	#barh("ATTRIBUTES", "Atributos")
	
	# keypoints
	#barh("KEYPOINTS", "Keypoints")
	
	# experimentos
	#barh("TASKS", "Experimentos de validação")
	
	# modelos de predicao
	#barh("PREDICTIVE_MODELS", "Modelos de predição")
	
if __name__ == "__main__":
	research_questions()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
