import webbrowser

with open("etapa2.bib_doi-list.txt") as doi:
	content = doi.readlines()
	
	for url in content:
		webbrowser.open_new_tab(url)

