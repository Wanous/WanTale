import flet as ft
from src.serveur.sushiscan import *
from src.pages.main_page import main_page
from src.tools.ConfigurationINI import INI
from src.tools.PDFreader import Book_reader


class Application:
    """
    Classe qui met en place l'application et regroupe les fonctionnalités de cette dernière
    tels que les changements de pages/onglets et importation de fichiers par exemple.
        """
    def __init__(self):

        #self.liste=images()
        self.ini=INI('assets/parameters.ini')
        self.book_reader=Book_reader(self)
        self.parameters=self.ini.charger()
        
    def main(self,page: ft.Page):
        self.page=page
        self.page.theme_mode=self.parameters['colors']['app_mode']
        self.page.theme=ft.Theme(color_scheme_seed=self.parameters['colors']['app_color'])

        #mise en place d'un scan pour trouver et stocker des livres
        self.directorys = self.parameters['directory']['all']
        self.directorys = self.directorys.split(",")
        self.liste_local=self.book_reader.general_scan(self.directorys)

        #récupération des livres mis en favoris 
        self.favorite_directorys = self.parameters['directory']['favorite']
        self.favorite_directorys = self.favorite_directorys.split(",")
        self.liste_favorite=self.book_reader.scan_favorite(self.favorite_directorys[1:])#Le premier indice contient rien

        #liste pour effectuer des recherches
        self.liste_search=[]
                
        #mise en place de moyen pour demander des fichiers
        self.file_picker = ft.FilePicker(on_result=self.on_dialog_result)
        self.page.overlay.append(self.file_picker)
        self.page.update()

        #mise en place de moyen pour changer de page
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

        #page de départ (onglet search)
        self.current_page = 0
        self.demarrage = main_page.onglet_search

    def on_dialog_result(self,e: ft.FilePickerResultEvent):
            print("Selected files:", e.files)
            print("Selected file or directory:", e.path)

    def menu_change(self,e):
            if type(e) != int : #If the change is by the navigation bar
                value = e.control.selected_index
                self.current_page = value
            

            #chaque chiffre est un identifiant vers un onglet du menu principale
            if self.current_page == 0:
                self.menu_page.onglet_search()
            if self.current_page == 1:
                  #self.page.go("/store")
                self.menu_page.onglet_local()
            elif self.current_page == 2 :
                self.menu_page.onglet_favorite()
            elif self.current_page == 3:
                #self.show_banner_click(e)
                self.menu_page.onglet_parameters()
            self.page.update()
    def close_banner(self,e):
            try :
                self.menu_page.banner.open = False
                self.page.update()
            except AttributeError :
                  print("non")

    def show_banner_click(self,e):
            self.menu_page.banner.open = True
            self.page.update()

    def return_home(self):
        print(self.current_page)
        self.menu_change(self.current_page)
        self.page.go("/")
        self.page.update()
        
    def route_change(self,route=None):
            """méthode pour changer de page"""
            self.page.views.clear()
            self.menu_page=main_page(self)
            self.page.views.append(
                ft.View(
                    "/",
                    self.menu_page.widgets,
                )
            )
            if self.page.route == "/book":
                self.page.views.append(
                    ft.View(
                        "/book",
                        [
                            ft.AppBar(title=ft.Text("book"), bgcolor=ft.colors.SURFACE_VARIANT),
                            ft.ElevatedButton("Go Home", on_click=lambda _: self.return_home()),
                        ],
                    )
                )
            self.page.update()

    def view_pop(self,view):
            """méthode pour revenir une page en arrière"""
            self.page.views.pop()          #suppression de la page dans la liste
            top_view = self.page.views[-1] #appelle de la page d'avant 
            self.page.go(top_view.route)   #affichage de celle-ci

    def snack_message(self,message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def change_theme(self,theme):
        if theme == '1':
            self.page.theme_mode='light'
        else:
             self.page.theme_mode='dark'
        
        self.ini.modifier('colors','app_mode',self.page.theme_mode)
        self.page.update()

    def change_color_scheme(self,color):
        self.page.theme=ft.Theme(color_scheme_seed=color)
        self.ini.modifier('colors','app_color',color)
        self.page.update()
    
    def add_favorite(self,e):
        e.control.selected = not e.control.selected #Change l'icône (sélectionnée/non sélectionnée)
        indice=int(e.control.content.value)         #Trouve l'indice de l'icône qui correspond à un livre
        book=self.liste_local[indice]
        
        #Si c'est pour ajouter un favoris
        if e.control.selected == True:
            self.liste_favorite.append(book) #ajoute le livre à la liste de favoris
            self.parameters['directory']['favorite']+=f',{book['directory']}/{book['name']}'
        else:
            self.liste_favorite.remove(book) #supprime le livre à la lidte de favoris
            self.parameters['directory']['favorite']=self.parameters['directory']['favorite'].replace(f',{book['directory']}/{book['name']}','')
            
        self.ini.modifier('directory','favorite',self.parameters['directory']['favorite']) #enregistre dans le ini
        e.control.update()                         #met à jour l'icône
    
    def search(self,e):
        self.liste_search=[]
        for books in self.liste_local:
             if e.data in books['name'] :
                  self.liste_search.append(books['name'])

        self.menu_page.searchbar.controls=[
                    ft.ListTile(title=ft.Text(name))
                    for name in self.liste_search
                    ]

        self.route_change()

         
app=Application()
ft.app(target=app.main)