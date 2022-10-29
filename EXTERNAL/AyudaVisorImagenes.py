""" Desarrollado por: Francisco Alejandro Medina.
e-mail: famedina@utp.edu.co

---------------------------------------
Visor de Imágenes
---------------------------------------
"""

from ctypes import alignment
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from PIL import ImageTk, Image

# Crear ventana Tk
window = Tk()
window.geometry('1024x720')
window.resizable(False, False)
window.title("Visor de imagenes")

# Variables de Control
Seleccion = IntVar(value=1)


# Función para explorar sistema de ficheros
# Retorna: ruta del fichero seleccionado
def OpenFile():
    file = filedialog.askopenfilename(filetypes=[
        ('Image Files JPG/JPEG', '*jpg'),
        ('Image Files JPG/JPEG', '*jpeg'),
        ('Image Files PNG', '*png'),
        ('Image Files GIF', '*gif')]
    )
    if (file != None and file != ""):
        imageRootEntry.delete(0, END)
        imageRootEntry.insert(0, file)
        CargarImagen()
    return file


# Procedimiento para cargar imágen en la ventana Tk
def CargarImagen():
    if (imageRootEntry.get() == ""):
        path = OpenFile()
    else:
        path = imageRootEntry.get()
    Imagen = Image.open(path)
    Imagen = Imagen.resize((700, 500), Image.LANCZOS) #maybe ANTIALIAS
    Imagen = ImageTk.PhotoImage(Imagen)
    analyzedImageLabel.configure(image=Imagen)
    window.mainloop()


# Boton para explorar ficheros
exploreFilesBtn = Button(window, text="Cargar Imagen", width=20, command=lambda: OpenFile())
exploreFilesBtn.grid(row=2, column=0, sticky=W)

# Caja para ruta del Archivo
imageRootEntry = Entry(window, width=90)
imageRootEntry.grid(row=2, column=1, columnspan=3, sticky=W)

# Label para mostrar Imagen
analyzedImageLabel = Label(image="", text="<< Imagen >>", foreground="white", anchor=CENTER, justify=CENTER,
                font=("Arial black", 50), pad=0)
analyzedImageLabel.grid(row=5, column=0, columnspan=3, sticky=W)
window.mainloop()
