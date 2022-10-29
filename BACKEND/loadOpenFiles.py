from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

path = ''

def exploreAndLoadFiles(window,imageRootEntry,analyzedImageLabel):
    """
    Nombre: exploreAndLoadFiles():
    Objetivo: Explorar y cargar el archivo de imagen a trabajar con el visor
    Parametros: window -> Instancia de Tkinter, la ventana que se abre al ejecutar el código
                imageRootEntry -> widget de caja de texto que almacena la ruta del archivo por abrir/cargar
                analyzedImageLabel -> widget etiqueta que permite almacena/posicionar la imagen dentro de la ventana del visro (windows)
    Retorna: El archivo de imagen cargado
    """
    file = filedialog.askopenfilename(filetypes=[
        ('Image Files JPG/JPEG', '*jpg'),
        ('Image Files JPG/JPEG', '*jpeg'),
        ('Image Files PNG', '*png'),
        ('Image Files GIF', '*gif')]
    )
    if (file != None and file != ""):
        imageRootEntry.delete(0, END)
        imageRootEntry.insert(0, file)
        loadFile(window,imageRootEntry,analyzedImageLabel)
    return file

def openFileGivenPath(window,imageRootEntry,analyzedImageLabel):
    """
    Nombre: openFileGivenPath():
    Objetivo: Carga el archivo de imagen a trabajar con el visor partiendo de que se debe de proporcionar la ruta, no se usará el administrador de archivos
                del sistema.
    Parametros: window -> Instancia de Tkinter, la ventana que se abre al ejecutar el código
                imageRootEntry -> widget de caja de texto que almacena la ruta del archivo por abrir/cargar
                analyzedImageLabel -> widget etiqueta que permite almacena/posicionar la imagen dentro de la ventana del visro (windows)
    Retorna: Lo que retorna loadFile()
    """
    loadFile(window, imageRootEntry, analyzedImageLabel)

def loadFile(window,imageRootEntry,analyzedImageLabel):
    """
    Nombre: loadFile():
    Objetivo: Carga el archivo de imagen a trabajar con el visor partiendo. Trabaja para las funciones anteriores
    Parametros: window -> Instancia de Tkinter, la ventana que se abre al ejecutar el código
                imageRootEntry -> widget de caja de texto que almacena la ruta del archivo por abrir/cargar
                analyzedImageLabel -> widget etiqueta que permite almacena/posicionar la imagen dentro de la ventana del visro (windows)
    Retorna: None
    """
    global path
    if (imageRootEntry.get() == ""):
        path = exploreAndLoadFiles(window,imageRootEntry,analyzedImageLabel)
    else:
        path = imageRootEntry.get()
    Imagen = Image.open(path)
    Imagen = Imagen.resize((800, 700), Image.LANCZOS) #maybe ANTIALIAS
    Imagen = ImageTk.PhotoImage(Imagen)
    analyzedImageLabel.configure(image=Imagen)
    window.mainloop()

def saveFile(editedImage):
    """
    Nombre: saveFile():
    Objetivo: Guarda la imagen editada en una ruta y con nombre especificados
    Parametros: editedImage -> Objeto de tipo Image (PIL) que contiene la imagen cargada y analizada en el visor
    Retorna: None
    """
    #First method, this apparently saves files into the directory where this function is called, in this case its from windows
    #also it onlly saves when ypu give from the code a specific name
    # editedImage.save('hhhh.jpeg')
    global path
    file = filedialog.asksaveasfile(mode='wb', defaultextension=".png", filetypes=(("PNG file", "*.png"),("JPEG file", "*.JPEG"),("JPG file", "*.jpg"),("All Files", "*.*")))
    if file:
        editedImage.save(file)
