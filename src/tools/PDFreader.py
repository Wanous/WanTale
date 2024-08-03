import fitz  # PyMuPDF
import os
import numpy as np
import base64
from io import BytesIO
from PIL import Image

class Book_reader:
    def __init__(self,master):
        self.master=master

    def general_scan(self,directorys):
        books=[]
        for directory in directorys:
            for folder in os.listdir(directory):
                file_liste = []
                for file in os.listdir(directory+'/'+folder):
                    file_liste.append(file)

                #Si il y a bien au moins un fichier dans le dossier
                if file_liste != []: 
                    cover = self.convert_pdf_to_images(directory+'/'+folder+'/'+file_liste[0])[0]
                    cover = self.convert_to_base64(cover)

                    #Alors le livre est rajouter
                    book = {'directory':directory,
                            'name':folder,
                            'files':file_liste,
                            'cover':cover}
                    books.append(book)
        
        if self.master != None :
            self.master.snack_message(f'{len(books)} livres scanné !')
        
        return books
    
    def scan_favorite(self,directorys):
        books=[]
        for directory in directorys:
                file_liste = []
                for file in os.listdir(directory):
                    file_liste.append(file)
                #Si il y a bien au moins un fichier dans le dossier
                if file_liste != []: 
                    cover = self.convert_pdf_to_images(directory+'/'+file_liste[0])[0]
                    cover = self.convert_to_base64(cover)

                    directory=directory.split('/')
                    #Alors le livre est rajouter
                    book = {'directory':(''.join(str(elem)+'/' for elem in directory[:-1]))[:-1] ,
                            'name':directory[-1],
                            'files':file_liste,
                            'cover':cover}
                    books.append(book)
        
        return books
    
    def convert_pdf_to_images(self,pdf_path):
        images = []
        with fitz.open(pdf_path) as pdf:
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
        return images
    
    def convert_to_base64(self,pil_photo):
        arr = np.asarray(pil_photo)
        pil_img = Image.fromarray(arr)
        buff = BytesIO()
        pil_img.save(buff, format="JPEG")

        newstring = base64.b64encode(buff.getvalue()).decode("utf-8")

        return newstring

    