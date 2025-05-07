import urllib.request
import pandas as pd
import bs4

url =  "https://www.comuni-italiani.it/province.html"
response = urllib.request.urlopen(url)
theBytes = response.read()
text = theBytes.decode("iso-8859-1")

doc = bs4.BeautifulSoup(text, "html.parser")
elems = doc.find_all("table")
table = elems[3]
lista = []
for tr in table.contents[2:-2]:
    if type(tr) == bs4.element.Tag:
        tds = tr.contents
        provincia = tds[1].get_text()
        residenti =  int(tds[2].get_text().replace(".",""))
        densita_ufficiale = float(tds[5].get_text().replace('.', '').replace(',', '.'))
        superficie = int(tds[4].get_text().replace(".",""))
        sigla = tds[7].get_text()
        lista.append([sigla, provincia, residenti, superficie, densita_ufficiale])

df =  pd.DataFrame(lista, columns=["Targa", "Provincia", "Residenti", "Superficie", "Densita_Ufficiale"])

df["Densità_Calcolata"] = (df["Residenti"] / df["Superficie"]).round(1)
df["Esito"] = df["Densità_Calcolata"] == df["Densita_Ufficiale"]
df["Esito"] = df["Esito"].map({True: "--", False: "differenza"})

df = df.sort_values(["Targa", "Provincia", "Residenti", "Densita_Ufficiale"])

print(df.drop(columns=["Superficie"]).to_string(index=False))

