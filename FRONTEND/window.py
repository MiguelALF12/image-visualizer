from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from PIL import ImageTk, Image
import BACKEND.loadOpenFiles
from BACKEND.loadOpenFiles import exploreAndLoadFiles,openFileGivenPath, saveFile
from BACKEND.ImageProccessing import *

image = 0

#----------------------------------------------------
#commands
class Commands():
    """

    1) --FUNCIONES COMMAND--

        NOMBRES Y FUNCIÓN: openFileGivenPathValidation() -> Abre un arhivo de imagen enviando como parametro interno la ruta ingresada en ImageEntryRoot
                            validate_entered_values(currentValues, defaultValues) -> Función de validación de los valores ingresados en el visor. si se han ingresado
                                                                                        valores, la suma total de cambios debe de ser menor a 8, caso cntrario donde sea igual (nunca será mayor)
                            re_load_image(imageToAnalize) -> Castea la imagen de np.asarrar() a imagen con codificación UTF-8, ademas de que modifica el tamaño de la imagen
                                                                y la dispone en un objeto ImageTK.PhotImage, necesario para cargarlo con Tkinter
                            update() -> Aplica todos los cambios ingresados en el visor a la imagen seleccionada
                            clear() -> Limpia las casillas y demas entradas de valores dentro del visor
                            disable_checkButtons() -> Función deshabilitadora de los checkbuttons usados para las capas de una imagen, esto debido a que solo es posible mostrar con
                                                        fidelidad una capa a ala vez.
        ARGUMENTOS DE LAS FUNCIONES: currentValues -> Lista de valores ingresados en cada widget dentro del visor
                                     defaultValues -> Valores asignados por defectos a los widget
                                     imageToAnalize -> imagen para analizar en formato np.asarray()
        RETORNOS: validate_entered_values(currentValues, defaultValues) -> Retorna la suma de todos los cambios-valores nuevos ingresados en los widgets del visor
                  update() -> Retorna None, para dar fina a la función

        ****IMPORTANTE****
            Estas funciones command trabajan internamente con parametros globales debido a que en su mayoría reciben un constante cambio

    2) Variables designadas para Tkinter

        window = Tk() -> Instancia de Tkinter. Ventana del visor
        inboxTitle = Label() -> Titulo en rojo "VISOR DE IMAGENES"
        exploreFilesLabel = Label() -> Etiqueta "Archivo de imagen" del area donde se situa la ruta de la imagen cargada
        imageRootEntry = Entry() -> Area de texto donde se situa la ruta de la imagen cargada
        analyzedImageLabel = Label() -> Etiqueta que alamcenará la imagen cargada
        exploreFilesBtn = Button() -> Boton que permite explorar los archivos de la maquina y escoger en donde se alamcena la imagen a manipular
        loadFilesBtn = Button() -> Boto que permite cargar una imagen ingresado en imageRootEntry la ruta absoluta de la misma
        brightnessLabel = Label() -> Etiqueta del campo que manipula el brillo
        brightnessSpinBox = Spinbox() -> widget que permite asignar valores en un rango de 1 a 100 para la caracteristica de brillo
        brightnessSlider = Scale() -> widget que permite asiganr valores en un rango de 1 a 100 para la caracteristica de brillo
        contrastLabel = Label() -> Etiqueta del campo que manipula el contraste
        contrastSpinBox = Spinbox() -> widget que permite asignar valores en un rango de 1 a 100 para la caracteristica de contraste
        contrastSlider = Scale() -> widget que permite asignar valores en un rango de 1 a 100 para la caracteristica de contraste
        whiteZone = Radiobutton() -> widget que permite selccionar el tipo de contraste a realizar, en este caso aumentar las zonas claras
        darkZone = Radiobutton() -> widget que permite selccionar el tipo de contraste a realizar, en este caso aumentar las zonas oscuras
        operationLabel = Label() -> Etiqueta del campo que manipula el tipo de operación (invertir color, zoom , girar) para aplicar a una imagen
        operationCombobox = Combobox() -> widget que permite selccionar el tipo de operacion a realizar, de entre estas estan: ('Seleccionar','Original','Brillo','F InvertColor','Zoom','Binarizado','Rotate')
        channelRGBlabel = Label() -> Etiqueta de los campos que indican los canales RGB de una imagen
        checkOptionRed = checkbutton() -> Widget que permite seleccionar en este caso la capa Roja de una imagen
        checkOptionGreen = checkbutton() -> Widget que permite seleccionar en este caso la capa Verde de una imagen
        checkOptionBlue = checkbutton() -> Widget que permite seleccionar en este caso la capa Azul de una imagen
        channelCMYKlabel = Label() -> Etiqueta de los campos que indican los canales CMYK de una imagen
        checkOptionCyan = checkbutton() -> Widget que permite seleccionar en este caso la capa Cyan de una imagen
        checkOptionMagenta = checkbutton() -> Widget que permite seleccionar en este caso la capa Magenta de una imagen
        checkOptionYellow = checkbutton() -> Widget que permite seleccionar en este caso la capa Amarilla de una imagen
        updateImageBtn = Button() -> Boton que aplicar los cambios ingresados al visor
        clearWidgetsBtn = Button() -> Boton que limpia los campos y resetea los valores por los valores default
        SaveWidgetsBtn = Button() -> Boton que permite guardar una imagen a la cual se le han realizado cambios


    3) diccionario de valores en la función update()

        values = {
            'brightSpinBox': brightnessSpinBox.get(), -> Obtiene el valor del campo al cual le aumentamos o disminuimos brillo
            'contrastSpinBox': contrastSpinBox.get(), -> Obtiene el valor del campo al cual le aumentamos o disminuimos contraste
            'brightslider': brightnessSlider.get(), -> Obtiene el valor del campo al cual le aumentamos o disminuimos brillo
            'contrastslider': contrastSlider.get(), -> Obtiene el valor del campo al cual le aumentamos o disminuimos contraste
            'darkWhiteZoneCheckBox': darkWhiteZonesoption.get(), -> Variable que almacena un entero indicando el tipo de contraste a realizar (1 para zonas claras y 2 para zonas oscuras)
            'typeCombobox': operationCombobox.get(), -> Obtiene el tipo de operación a realizar (invertir color, zoom, girar, etc)
            'channelsRGB': [red.get(),green.get(),blue.get()], -> Obtiene el valor de cada uno de los chekcbutton que indican un canal (RGB). Si es 1 indica que esa capa se quiere mostrar, caso contrario si es cero
            'channelsCMYK':[cyan.get(),magenta.get(),yellow.get()] -> Obtiene el valor de cada uno de los chekcbutton que indican un canal (CMYK). Si es 1 indica que esa capa se quiere mostrar, caso contrario si es cero
        }

    """

    @staticmethod
    def openFileGivenPathValidation():
        global imageRootEntry

        if imageRootEntry.get() != '':
            openFileGivenPath(window,imageRootEntry,analyzedImageLabel)
        else:
            messagebox.showinfo(title="ALERTA!!", message="Debe de propocionar la ruta de la imagen que desea cargar!!")

    @staticmethod
    def validate_entered_values(currentValues, defaultValues):
        flag = 0
        for value in currentValues:
            if value in defaultValues:
                flag += 1
        return flag

    @staticmethod
    def re_load_image(imageToAnalize):
        global analyzedImageLabel, image
        updatedImage = Image.fromarray(np.uint8(imageToAnalize))
        updatedImage = updatedImage.resize((800, 700), Image.LANCZOS)
        image = updatedImage
        updatedImage = ImageTk.PhotoImage(updatedImage)
        analyzedImageLabel.configure(image=updatedImage)
        window.mainloop()

    @staticmethod
    def update():
        global brightnessSpinBox,contrastSpinBox,brightnessSlider,contrastSlider,darkWhiteZonesoption,operationCombobox, analyzedImageLabel,red,green,blue,cyan,magenta,yellow
        imagePath = BACKEND.loadOpenFiles.path
        values = {
            'brightSpinBox': brightnessSpinBox.get(),
            'contrastSpinBox': contrastSpinBox.get(),
            'brightslider': brightnessSlider.get(),
            'contrastslider': contrastSlider.get(),
            'darkWhiteZoneCheckBox': darkWhiteZonesoption.get(),
            'typeCombobox': operationCombobox.get(),
            'channelsRGB': [red.get(),green.get(),blue.get()],
            'channelsCMYK':[cyan.get(),magenta.get(),yellow.get()]
        }
        defaultValues = ['', '', 0, 0, 0, 'Seleccionar', [0, 0, 0], [0, 0, 0]]
        currentValues = values.values()
        flag=Commands.validate_entered_values(currentValues, defaultValues)
        updatedImage = ''
        if imagePath != "":
            imageToAnalize = np.asarray(Image.open(imagePath))
            if flag == 8:
                messagebox.showinfo(title="ALERTA!!", message="No has ingresado ningún cambio!!")
                Commands.re_load_image(imageToAnalize)
            else:
                if values['brightSpinBox'] != '':
                    brightnessFactor = int(values['brightSpinBox'])
                    updatedImage = manageBrigthness(imageToAnalize, brightnessFactor)

                if values['contrastSpinBox'] != '':
                    contrastFactor = int(values['contrastSpinBox'])
                    if values['brightSpinBox'] != '':
                        if values['brightSpinBox'] > str(0):
                            foo = float(values['brightSpinBox'])
                        else:
                            foo = float(1)
                    else:
                        foo = float(5)

                    if values['darkWhiteZoneCheckBox'] == 0:
                        messagebox.showinfo(title="ALERTA!!",message="Debe de escoger el tipo de contraste (zonas claras o zonas oscuras)")
                    else:
                        updatedImageAux = imageToAnalize * float(foo) / 50
                        updatedImage = manageContrast(updatedImageAux, values['darkWhiteZoneCheckBox'], contrastFactor)

                if values['typeCombobox'] == 'Original':
                    updatedImage = imageToAnalize
                elif values['typeCombobox'] == 'Brillo':
                    messagebox.showinfo(title="Valores definidos",
                                        message="Se usará de brillo igual 15 como valor default \n a menos que ingrese algún valor en la casilla de brillo!!")
                    if values['brightSpinBox'] != '':
                        brightnessFactor = int(values['brightSpinBox'])
                    else:
                        brightnessFactor = int(15)
                    updatedImage = manageBrigthness(imageToAnalize, brightnessFactor)
                elif values['typeCombobox'] == 'F InvertColor':
                    updatedImage = inverse(imageToAnalize)
                elif values['typeCombobox'] == 'Zoom':
                    messagebox.showinfo(title="Valores definidos",message= "Se usará como valor default de .5 de aumento para la posición x=100,y=100")
                    updatedImage = zoomImage(imageToAnalize, 0.5, [100, 100])
                elif values['typeCombobox'] == 'Binarizado':
                    updatedImage = binarize(imageToAnalize, [0, 128])
                elif values['typeCombobox'] == 'Rotate':
                    messagebox.showinfo(title="Valores definidos",
                                        message="Se usará como valor default de angulo de rotación igual a 10 grados")
                    updatedImage = Rotate(imageToAnalize, 10)

                if values['channelsRGB'] != 0:
                    if values['channelsRGB'][0] == 1:
                        updatedImage = rgb(imageToAnalize, 0)
                    elif values['channelsRGB'][1] == 1:
                        updatedImage = rgb(imageToAnalize, 1)
                    elif values['channelsRGB'][2] == 1:
                        updatedImage = rgb(imageToAnalize, 2)

                if values['channelsCMYK'] != 0:
                    if values['channelsCMYK'][0] == 1:
                        updatedImage = cmyk(imageToAnalize, 0)
                    elif values['channelsCMYK'][1] == 1:
                        updatedImage = cmyk(imageToAnalize, 1)
                    elif values['channelsCMYK'][2] == 1:
                        updatedImage = cmyk(imageToAnalize, 2)
            Commands.re_load_image(updatedImage)
        else:
            messagebox.showinfo(title="ALERTA!!", message="No has cargado imagenes!!")

        return

    @staticmethod
    def clear():
        global brightnessSpinBox, contrastSpinBox, brightnessSlider, contrastSlider, darkWhiteZonesoption, operationCombobox, analyzedImageLabel, red, green, blue, cyan, magenta, yellow

        defaultValues = ['', '', 0, 0, 0, 'Seleccionar', [0, 0, 0], [0, 0, 0]]
        currentValues = [brightnessSpinBox.get(),
        contrastSpinBox.get(),
        brightnessSlider.get(),
        contrastSlider.get(),
        darkWhiteZonesoption.get(),
        operationCombobox.get(),
        [red.get(), green.get(), blue.get()],
        [cyan.get(), magenta.get(), yellow.get()]
        ]
        flag = Commands.validate_entered_values(currentValues,defaultValues)
        if flag == 8:
            messagebox.showinfo(title="ALERTA!!", message="No has ingresado ningún cambio. No hay nada que limpiar!!")
        else:
            brightnessSpinBox.set('')
            contrastSpinBox.set('')
            brightnessSlider.set(0)
            contrastSlider.set(0)
            darkWhiteZonesoption.set(0)
            operationCombobox.current(0)
            red.set(0)
            green.set(0)
            blue.set(0)
            cyan.set(0)
            magenta.set(0)
            yellow.set(0)
            checkOptionRed.configure(state="active")
            checkOptionGreen.configure(state="active")
            checkOptionBlue.configure(state="active")
            checkOptionCian.configure(state="active")
            checkOptionMagenta.configure(state="active")
            checkOptionYellow.configure(state="active")

            imagePath = BACKEND.loadOpenFiles.path
            if imagePath != '':
                imageToAnalize = np.asarray(Image.open(imagePath))
                Commands.re_load_image(imageToAnalize)

    @staticmethod
    def disable_checkButtons():
        global red,green,blue,cyan,magenta,yellow, checkOptionRed, checkOptionGreen,checkOptionBlue, checkOptionCian, checkOptionMagenta, checkOptionYellow
        channelsRGBCMYK = [(red.get(),checkOptionRed), (green.get(),checkOptionGreen), (blue.get(),checkOptionBlue),(cyan.get(),checkOptionCian), (magenta.get(),checkOptionMagenta), (yellow.get(),checkOptionYellow)]
        flagRGBSMYK = [False,0]

        for item_validation, object in channelsRGBCMYK:
            if item_validation == 1:
                flagRGBSMYK[0] = True
                flagRGBSMYK[1] = object
            else:
                object.configure(state='active')

            if flagRGBSMYK[0]:
                for _,object in channelsRGBCMYK:
                    if object != flagRGBSMYK[1]:
                        object.configure(state='disabled')
#----------------------------------------------------

#----------Componentes visuales del visor------------

# Ventana
window = Tk()
window.geometry('1420x850')
window.resizable(False, False)
window.title("Visor de imagenes")


#-----ruta de imagen, botones de carga y explorar, label que almacena imagen-----
inboxTitle = Label(window,text="VISOR DE IMAGENES", foreground="red",background="white" ,font=("Arial", 40))
inboxTitle.grid(row=0,column=5, pady=15)

exploreFilesLabel = Label(window,text="Archivo de imagen", foreground="black", font=("Arial black", 12))
exploreFilesLabel.grid(row=1,column=0, padx=100)

imageRootEntry = Entry(window, width=60)
imageRootEntry.grid(row=1,column=1, sticky='w',columnspan=5, padx=20)

analyzedImageLabel = Label(window,image="",text="",width=80)
analyzedImageLabel.place(x=60,y=130)

exploreFilesBtn = Button(window, text="Explorar", width=12, command=lambda: exploreAndLoadFiles(window,imageRootEntry,analyzedImageLabel))
exploreFilesBtn.grid(row=1, column=6, padx=4, pady=5)

loadFilesBtn = Button(window, text="Cargar", width=12, command=lambda: Commands.openFileGivenPathValidation())
loadFilesBtn.grid(row=1, column=7, padx=5, pady=5)

#--------------------------------------------------------------------------------

#----------Brillo y contraste-------------

brightnessLabel = Label(text="Brillo", foreground="black", font=("Arial:", 15))
brightnessLabel.grid(row=2, column=6, sticky='w', padx=10, pady=15)

brightnessSliderVariable = IntVar()
brightnessSlider = Scale(window,from_=0, to=100, orient ='horizontal',length=80)
brightnessSlider.grid(row=2,column=8, padx=20)

brightnessSpinBox = Spinbox(window, state='readonly', from_=0, to=100)
brightnessSpinBox.grid(row=2,column=7)


contrastLabel = Label(text="Contraste:", foreground="black",font=("Arial", 15))
contrastLabel.grid(row=3,column= 6, sticky='nw', padx=10, pady=10)

contrastSpinBox = Spinbox(window,state='readonly', from_ = 0, to = 100)
contrastSpinBox.grid(row=3,column=7,sticky='w')

contrastSlider = Scale(window, from_=0, to=100,  orient='horizontal', length=80)
contrastSlider.grid(row=3,column=8, padx=20)

darkWhiteZonesoption = IntVar()
whiteZone = Radiobutton(window,text='Zonas claras',value=1,variable=darkWhiteZonesoption,width=10)
whiteZone.grid(row=4,column=7, pady=15, padx=5)

darkZone = Radiobutton(window,text='Zonas oscuras',value=2,variable=darkWhiteZonesoption,width=10)
darkZone.grid(row=4,column=8, padx=10, pady=15, sticky='w')
#-----------------------------------------

#-----------Tipos de funciones-------------

operationLabel = Label(window, text="Tipo:", font= ("Arial Bold",15))
operationLabel.grid(row=5, column=6,pady=20)

operationCombobox = Combobox(window,values=('Seleccionar','Original','Brillo','F InvertColor','Zoom','Binarizado','Rotate'),state='readonly',takefocus=False)
operationCombobox.current(0) #item seleccionado, en este caso 'Original'
operationCombobox.grid(row=5,column=7)
#------------------------------------------

#-----------Canales RGB y CMYK-----------

#RGB
channelRGBlabel = Label(window, text="Canales RGB:", font= ("Arial",15))
channelRGBlabel.grid(row=6,column=6,pady=10,sticky='w')

red = IntVar()
green = IntVar()
blue = IntVar()

checkOptionRed = Checkbutton(window, text = "RED: ", width=5, variable=red,command=lambda:Commands.disable_checkButtons())
checkOptionRed.grid(column = 7, row = 6, sticky='w')
checkOptionGreen = Checkbutton(window, text = "GREEN: ", width=5, variable=green,command=lambda:Commands.disable_checkButtons())
checkOptionGreen.grid(column = 7, row = 7,pady=10,sticky='w')
checkOptionBlue = Checkbutton(window, text = "BLUE: ", width= 5, variable=blue,command=lambda:Commands.disable_checkButtons())
checkOptionBlue.grid(column = 7, row = 8,pady=10, sticky='w')

#CMYK
channelCMYKlabel = Label(window, text="Canales CMYK:", font= ("Arial",15))
channelCMYKlabel.grid(row=9,column=6,pady=10,sticky='w')

cyan = IntVar()
magenta = IntVar()
yellow = IntVar()

checkOptionCian = Checkbutton(window, text = "CYAN: ", width=5, variable=cyan, command=lambda: Commands.disable_checkButtons())
checkOptionCian.grid(column = 7, row = 9, sticky='w')
checkOptionMagenta = Checkbutton(window, text = "MAGENTA: ", width=5, variable=magenta, command=lambda:Commands.disable_checkButtons())
checkOptionMagenta.grid(column = 7, row = 10,pady=10,sticky='w')
checkOptionYellow = Checkbutton(window, text = "YELLOW: ", width= 5, variable=yellow,command=lambda:Commands.disable_checkButtons())
checkOptionYellow.grid(column = 7, row = 11,pady=10, sticky='w')
#----------------------------------------

#----------Botones de actualizar, limpiar y guardar----------

updateImageBtn = Button(window, text="Actualizar", width=12, command=lambda: Commands.update())
updateImageBtn.grid(row=12, column=6,pady=10)

clearWidgetsBtn = Button(window, text="Limpiar", width=10, command=lambda:Commands.clear())
clearWidgetsBtn.grid(row=12, column=7, pady=10)

SaveWidgetsBtn = Button(window, text="Guardar", width=10, command=lambda: saveFile(image))
SaveWidgetsBtn.grid(row=13, column=6, pady=10)
#------------------------------------------------------------

# window.mainloop()

