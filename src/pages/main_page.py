import flet as ft
from flet_contrib.color_picker import ColorPicker

class main_page:     
    def __init__(self,master): 
        self.master=master
        self.widgets = self.create_widgets()
        self.name='main menu'

    def create_widgets(self):
        #Barre de navigation
        self.navigation=ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            indicator_shape=ft.CircleBorder("circle"),
            min_extended_width=400,
            leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add",on_click=lambda _: self.master.file_picker.pick_files(allow_multiple=True)),
            group_alignment=-0.9,
            destinations=[
                 ft.NavigationRailDestination(
                    icon=ft.icons.SEARCH, 
                    selected_icon=ft.icons.SAVED_SEARCH_OUTLINED, 
                    label="Search",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.BOOK_OUTLINED, 
                    selected_icon=ft.icons.BOOK, 
                    label="Local",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Favorite",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],
            on_change=lambda e:self.master.menu_change(e)
        )
        #Initialise de la colonne de l'onglet et de ses paramètres
        self.onglet_show = ft.Column(scroll='always') 

        #barre de recherche
        self.searchbar = ft.SearchBar(       
                        divider_color=ft.colors.AMBER,
                        bar_hint_text="Search colors...",
                        on_change=lambda e:print(e.control['value']))

        #Structuration de la page au sein d'un widget row --> navigation | onglet
        self.row=ft.Row([self.navigation,ft.VerticalDivider(width=1),self.onglet_show],expand=True)

        #Bannière pour afficher les erreurs d'importations ou autres 
        self.banner=ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                "Oops, there were some errors while trying to delete the file. What would you like me to do?"
            ),
            actions=[
                ft.TextButton("Retry", on_click=self.master.close_banner),
                ft.TextButton("Ignore", on_click=self.master.close_banner),
                ft.TextButton("Cancel", on_click=self.master.close_banner),
            ],
        )

        #onglet de démarrage/par défaut (décider depuis le fichier main.py)
        self.master.demarrage(self)

        #Retourne ce qui doit être afficher
        return [self.row,self.banner]
    
    def onglet_search(self):
         self.row.controls[2].controls=[self.searchbar]
    #Onglets du menu principale (indice 2 dans l'application)
    def onglet_local(self):
        #Si une recherche est en court
        recherche = self.master.liste_local
        self.navigation.leading.disabled=False

        
        self.row.controls[2].controls=[ft.Column(
                                ft.Stack(
                                [ft.Image(
                                    src_base64=img,
                                    width=300,
                                    height=300,
                                    fit=ft.ImageFit.CONTAIN,
                                    border_radius=0
                                        ),

                                ft.CupertinoButton(
                                    content=ft.Text(value=str(i), color = ft.colors.with_opacity(0.0, '#ff6666')),
                                    opacity_on_click=0.3,
                                    on_click=lambda e:self.master.page.go("/book"),
                                    #on_click=lambda e: print("Book n°"+str(e.control.content.value)+":"+self.master.liste_local[int(e.control.content.value)]['name']),
                                    min_size=300,
                                    color = ft.colors.with_opacity(0.0, '#ff6666')
                                ),
                                                                               
                                ft.IconButton(
                                    content=ft.Text(value=str(i)),
                                    icon=ft.icons.FAVORITE_BORDER,
                                    selected_icon=ft.icons.FAVORITE,
                                    icon_size=25,
                                    tooltip="Favorite",
                                    on_click=lambda e :self.master.add_favorite(e),
                                    selected=False if recherche[i] not in self.master.liste_favorite else True,
                                            ),
 
                                ])   for i,img in enumerate(t['cover'] for t in recherche))          
                                ]
        self.row.controls[2].controls[0].alignement=ft.MainAxisAlignment.CENTER
        #self.row.controls[2].controls[0].expand=True

    def onglet_favorite(self):
        self.navigation.leading.disabled=True
        self.row.controls[2].controls=[ft.Stack(
                                [ft.Image(
                                    src_base64=img,
                                    width=300,
                                    height=300,
                                    fit=ft.ImageFit.CONTAIN,
                                    border_radius=50
                                        )                            
                                ])  for i,img in enumerate(t['cover'] for t in self.master.liste_favorite)]
        
    def onglet_parameters(self):
        self.navigation.leading.disabled=True
        self.colorpicker = ColorPicker(color='#ffffff',width=200)      
        self.color_container = ft.Container(content=ft.Text(value='Change the color ',scale=1.5, weight=ft.FontWeight.W_900))
        self.color_container.margin = ft.margin.only(left=40)

        self.app_mode_container = ft.Container(content=ft.Text(value='Change theme',scale=1.5, weight=ft.FontWeight.W_900))
        self.app_mode_container.margin = ft.margin.all(40)

        self.row.controls[2].controls=[self.color_container
                                       ,
                                       ft.Divider(),
                                       self.colorpicker,
                                       ft.FilledTonalButton("Save", 
                                                            icon=ft.icons.SAVE_AS,
                                                            on_click=lambda e:self.master.change_color_scheme(self.colorpicker.color)),
                                       ft.Divider(),
                                       self.app_mode_container,
                                       ft.CupertinoSlidingSegmentedButton(
                                                    selected_index=1,
                                                    on_change=lambda e:self.master.change_theme(e.data) ,
                                                    padding=ft.padding.symmetric(0, 10),
                                                    controls=[
                                                        ft.Text("dark"),
                                                        ft.Text("light"),
                                                    ],
                                                ),]







