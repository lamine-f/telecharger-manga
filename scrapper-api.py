#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import cgitb
import cgi
import json
import concurrent.futures

   
class GetLelscans():

    def __init__(self):
        self.url = "https://lelscans.net/lecture-ligne-one-piece"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.mangasNames = self.getNames(self.getLinks(self.soup))
        self.namesAndLinks = self.getNamesAndLinks()
    

    def getLinks(self, soup):
        if self.response.ok: 
            soup = self.soup
            links = []
            for html_option in soup.find_all("option"):
                option_value = html_option.get('value')
                if (not("scan-one-piece" in option_value.split("/"))):
                    links.append(option_value)
            return links

    def getNames(self, links):
        names = []
        for link in links:
            name = link.split("/")[-1].split("ligne")[-1].replace("-", " ").replace(".php", "").strip()
            names.append(name)
        return { i+1 : names[i] for i in range(len(names))}

    def getNamesAndLinks(self):
        if self.response.ok:    
            soup = self.soup
            links = self.getLinks(soup)
            return { self.mangasNames[i+1] : links[i] for i in range(len(links)) }


    def changeLinkToRealUseFullLink(self, response):
        if response.ok:
            soup2 = BeautifulSoup(response.text, 'html.parser')
            return soup2.select("a[class=active]")[0].get("href")


    def getPictureContent(self, Link):
        response = requests.get(Link)
        soup = BeautifulSoup(response.text, "html.parser")
        src = "http://lelscans.net" + str(soup.find("img").get("src"))
        return requests.get(src).content



    def download_image(self, url, filename):
        # Télécharger l'image à partir de l'URL et enregistrer dans le fichier
        image_content = self.getPictureContent(url)
        with open(filename, "wb") as f:
            f.write(image_content)

    def download_images_parallel(self, scanLink, folderName, top, bottom):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Liste des futures (résultats) des tâches en cours d'exécution
            futures = []

            for i in range(top, bottom+1):
                # Construire le nom complet du fichier
                fullFicName = folderName + "/" + str(i)
                # Créer une tâche pour télécharger chaque image en parallèle
                future = executor.submit(self.download_image, scanLink+str(i), fullFicName)
                futures.append(future)

            # Attendre la fin de toutes les tâches et récupérer les résultats
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    # Traiter le résultat si nécessaire
                except Exception as e:
                    # Gérer les exceptions si elles se produisent pendant l'exécution de la tâche
                    print("Une exception s'est produite :", e)
    
    def downloadManga(self, choice, top, bottom):
        #Récuperer le lien du manga selectionné
        scanLink = self.changeLinkToRealUseFullLink(requests.get(self.namesAndLinks[self.mangasNames[choice]]))[:-1]
        
        PATH = os.path.abspath("datas")
        slugName = self.mangasNames[choice].replace(' ', '_').strip()
        folderName = PATH + "/" + slugName

        try:
            os.mkdir(folderName)
        except:
            pass

        self.download_images_parallel(scanLink, folderName, top, bottom)
        
        """
        for i in range(top, bottom+1):
            fullFicName = folderName + "/" + str(i)
            with open(fullFicName, "wb") as f:
                f.write(self.getPictureContent(scanLink+str(i)))
        """

def toArray(dict_array):
    return list(dict_array)


print("Content-Type: application/json\n\n")
cgitb.enable()

Request = {}
req = cgi.FieldStorage()
for key in req.keys():
    Request[key] = req[key].value

RequestKeys = toArray(Request.keys())
RequestValues = toArray(Request.values())  

lelscanOb = GetLelscans()

if ("getMangasName" in RequestValues):
    print(json.dumps(lelscanOb.mangasNames))

elif ("choice" in RequestValues):
    value = int(Request["value"])
    value1 = int(Request["value1"])
    value2 = int(Request["value2"])
    lelscanOb.downloadManga(value, value1, value2)
    print(json.dumps({'status': 1}))
else:
    pass
