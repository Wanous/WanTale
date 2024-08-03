import requests
from bs4 import BeautifulSoup

class Manga:
    def __init__(self,url):
        self.url=url
        self.manga=self.extraction(self.url)
        
    def extraction(self,url):
        reponse = requests.get(url)                          # Effectue une requête GET pour récupérer le contenu HTML de l'URL
        liste = []                                           #Liste des noms des chapitres 
        
        if reponse.status_code == 200:                       # Vérifie si la requête a réussi (code d'état 200)
            soup = BeautifulSoup(reponse.text, 'html.parser')# Analyse le contenu HTML avec BeautifulSoup    
            balises_paragraphes = soup.find_all('a')         # Trouve toutes les balises <a> (paragraphes) dans le HTML
            
            # Affiche le contenu des balises <a>
            for balise_a in balises_paragraphes:
                chap=balise_a.find('span', class_='chapternum')

                if chap != None:
                    infos={'nom':chap.get_text(),'lien':balise_a.get('href')}
                    liste.append(infos)
            return liste
        else:
            print("Échec de la requête. Code d'état :", reponse.status_code)
            return liste
        
    def informations(self):
        for c in range(len(self.manga)) :
            print('')
            for cle,value in self.manga[c].items():
                print(cle,':',value)

        


def get_image(url):
        reponse = requests.get(url)                        
        liste = []                                          
        
        if reponse.status_code == 200:                    
            soup = BeautifulSoup(reponse.text, 'html.parser') 
            balises_paragraphes = soup.find_all('img')      
            
            for balise_img in balises_paragraphes:
                B = balise_img.get('data-src')
                if 'scans' in B :
                    liste.append(balise_img.get('data-src'))

            return liste
        else:
            print("Échec de la requête. Code d'état :", reponse.status_code)
            return liste   
        
def fichier_html(nom,contenu):
    with open(nom, 'w', encoding='utf-8') as fichier:
        fichier.write(contenu)
    
if __name__ == "__main__":
    url = "https://sushiscan.fr/manga/spy-x-family"
    test=Manga(url)
    test.informations()
    
    liens=[i['lien'] for i in test.manga]
    for t in liens:
        #print(t)
        pass
    #message : il y a un probléme avec le première indice
    #print(liens[0])
    del liens[0]
    print(get_image(liens[2]))
    
    truc =''
    for image in get_image(liens[len(test.manga)-2]):
        truc+='<img src='+image+'>'
    print(truc)
    fichier_html("test.html",truc)

    

