import seaborn
import pandas as pd
import matplotlib.pyplot as plt

semduplicados = [638, 379, 510]
ieee = [225, 92, 102]
acm = [42, 25, 34]
scopus = [387, 91, 152]
webofscience = [375, 254, 321]
x = [1, 2, 3]

seaborn.set()

plt.plot(x, semduplicados, label="Sem dubplicados")
plt.plot(x, webofscience, label="Web of Science")
plt.plot(x, scopus, label="Scopus")
plt.plot(x, ieee, label="IEEE Xplore")
plt.plot(x, acm, label="ACM Digital Library")

for i, j in zip(x, semduplicados):
	plt.annotate(str(j), xy=(i, j+5))

for i, j in zip(x, ieee):
	plt.annotate(str(j), xy=(i, j+5))

for i, j in zip(x, acm):
	plt.annotate(str(j), xy=(i, j+5))

for i, j in zip(x, scopus):
	plt.annotate(str(j), xy=(i, j+5))

for i, j in zip(x, webofscience):
	plt.annotate(str(j), xy=(i, j+5))

plt.title("Resultados por Versão de String de Busca")
plt.xticks(x, ("V1", "V2", "V3"))
plt.ylim(0, 700)
plt.legend()
plt.show()

