
import numpy as np
import math

def manageBrigthness(image,factor):
    """
    Nombre:manageBrigthness(image,factor)
    Objetivo: Manejar (cambiar) el brillo de una imagen
    Parametros: image -> Una imagen jpg o jpeg para mac), o png. Si es jpg se recomienda
                            dividirla sobre 255 pra manejar valores entre 0 y 1.
                factor -> Factor por el cual se decide si la imagen aumenta o disminuye de brillo. Funciona sumandole este factor a cada uno de
                            los pixeles de la imagen
    Retorna: La imagen con el brillo configurado
    """
    #factor use values from -100 to 100 in every layer of RGB composition
    managedImage = image + factor
    return managedImage

def manageContrast(image,type,factor):
    """
    Nombre: manageContrast(image,type,factor):
    Objetivo: Manejar (cambiar) el contraste de una imagen (diferencia entre un tono de color respecto a los otros)
    Parametros: image -> Una imagen jpg o jpeg para mac), o png. Si es jpg se recomienda
                            dividirla sobre 255 pra manejar valores entre 0 y 1.
                type -> Define el tipo de contraste a realizar:
                             - Contraste de las zonas oscuras en detrimento de las zonas claras.
                             - contraste de las zonas claras en detrimento de las oscuras.
                factor -> Factor por el cual se decide si la imagen aumenta o disminuye el contraste
    Retorna: La imagen con el contraste configurado
    """

    if type == 1:
        image = factor*np.log10(1+image)
    elif type == 2:
        image = factor*np.exp(image-1)
    return image

def inverse(image):
    """
    Nombre: inverse(image)
    Objetivo: invertir el color de una imagen
    Parametros: image -> imagen de un fondo blanco en formato png o jpg (jpeg para mac)
    Retorna: La imagen con sus colores invertidos
    """
    inversedImage = 255 - image
    return inversedImage

def zoomImage(image,percentage, coordenates):
    """
    Nombre: zoomImage(image,percentage, coordenates)
    Objetivo: Realizar zoom (aumento) a una imagen
    Parametros: image -> Una imagen jpg o jpeg para mac), o png.
                percentage -> indica la relación de aumento que se quiere hacer por cada punto de la imagen. Cuanto se quiere hacer de zoom a la imagen
                coordenates -> Punto dentro de la imagen al cual se le quiere hacer zoom
    Retorna: La imagen zoomeada.
    """
    #percentage <= 100 (need to give from 0.0 to 1.0, [x,y] are both coordenates of the point of zoom; greather than zero and less than the size of the image
    # new_image = np.zeros((image.shape[0],image.shape[1],image.shape[2]))
    new_image = np.copy(image)
    x = coordenates[0]
    y = coordenates[1]
    zoomedImage = np.copy(new_image)
    for row in range(0,new_image.shape[0]):
        for col in range(0,new_image.shape[1]):
            originalImageRow = round(percentage*row+x)
            originalImageCol = round(percentage*col+y)
            zoomedImage[row,col] = image[originalImageRow,originalImageCol]
    return zoomedImage

def binarize(image,umbral):
    """
    Nombre: zoomImage(image,percentage, coordenates)
    Objetivo: Realizar zoom (aumento) a una imagen
    Parametros: image -> Una imagen jpg o jpeg para mac), o png.
                percentage -> indica la relación de aumento que se quiere hacer por cada punto de la imagen. Cuanto se quiere hacer de zoom a la imagen
                coordenates -> Punto dentro de la imagen al cual se le quiere hacer zoom
    Retorna: La imagen zoomeada.
    """
    capaRoja = image[:, :, 0]
    capaVerde = image[:, :, 1]
    capaAzul = image[:, :, 2]
    averagedImage = 0.2989 * capaRoja + 0.5870 * capaVerde + 0.1140 * capaAzul
    # plt.imshow(averagedImage)
    # plt.show()
    image[:, :, 0] = averagedImage
    image[:, :, 1] = averagedImage
    image[:, :, 2] = averagedImage
    averagedImage[averagedImage > umbral[0]]= 255
    averagedImage[averagedImage < umbral[1]] = 0
    image[:, :, 0] = averagedImage
    image[:, :, 1] = averagedImage
    image[:, :, 2] = averagedImage

    return image

def Rotate(img, angDegrad):
    """
    Nombre: Rotate(img, alpha)
    Objetivo: Rotar la imagen entregada
    Parametros: img-> Una imagen jpg o jpeg para mac), o png.
                alpha -> un numero entero que indica el angulo el cual se quiere rotar la imagen. Se usa la función Degra_rad(angDegrad) para convertir
                            el entero a unidades de radianes
    Retorna: La imagen rotada
    """
    h, w, c = np.shape(img)
    alpha = angDegrad * math.pi / 180
    inv_affine_matrix = np.linalg.inv(
        np.array([[math.cos(alpha), math.sin(alpha), 0], [-math.sin(alpha), math.cos(alpha), 0], [0, 0, 1]]))
    new_img = np.zeros_like(img)
    for c_idx in range(c):
        for ny_idx in range(h):
            for nx_idx in range(w):
                v = np.matmul(np.array([ny_idx, nx_idx, 1]), inv_affine_matrix)
                y_idx = v[0]
                x_idx = v[1]
                new_img[ny_idx, nx_idx, c_idx] = img[int(y_idx) % h, int(x_idx) % w, c_idx]

    return new_img

def rgb(MiImagen,layer_to_show):
    """
    Nombre: rgb(MiImagen,use_option,layer_to_show):
    Objetivo: Mostrar las capas de colores de una imagen. Capas en formato RGB
    Parametros: MiImagen -> imagen de un fondo blanco en formato png o jpg (jpeg para mac)
                use_option -> Indica el uso de la función, es decir, si retorna o no información, en este caso la imagen según la capa indicada
                layer_to_show -> recibe la capa que se quiere visualizar ((0,roja),(1,verde),(2,azul)))
    Retorna: La capa de colores de la imagen
    Nota: si use_option es 2 se retorna la imagen divididad en sus capas.
    """

    # Capa roja
    CapaRoja = np.copy(MiImagen)
    CapaRoja[:, :, 1] = 0  # Indica que la capa verde sea cero
    CapaRoja[:, :, 2] = 0  # Indica que la capa azul sea cero

    # Capa verde
    CapaVerde = np.copy(MiImagen)
    CapaVerde[:, :, 0] = 0
    CapaVerde[:, :, 2] = 0

    # Capa azul
    CapaAzul = np.copy(MiImagen)
    CapaAzul[:, :, 0] = 0
    CapaAzul[:, :, 1] = 0
    if layer_to_show == 0:
        return CapaRoja
    elif layer_to_show == 1:
        return CapaVerde
    elif layer_to_show == 2:
        return CapaAzul

def cmyk(MiImagen,layer_to_show):
    """
    Nombre: cmyk(MiImagen,use_option,layer_to_show)
    Objetivo: Mostrar las capas de colores de una imagen. Capas en formato CMYK
    Parametros: MiImagen -> imagen de un fondo blanco en formato png o jpg (jpeg para mac)
                use_option -> Indica el uso de la función, es decir, si retorna o no información, en este caso la imagen según la capa indicada
                layer_to_show -> recibe la capa que se quiere visualizar ((0,cian),(1,magenta),(2,amarillo)))
    Retorna: La capa de colores de la imagen
    """
    CapaCian = np.copy(MiImagen)
    CapaCian[:, :, 1] = 255
    CapaCian[:, :, 2] = 255
    # Capa magenta
    CapaMagenta = np.copy(MiImagen)
    CapaMagenta[:, :, 0] = 255
    CapaMagenta[:, :, 2] = 255

    # Capa Yellow
    CapaYellow = np.copy(MiImagen)
    CapaYellow[:, :, 0] = 255
    CapaYellow[:, :, 1] = 255

    if layer_to_show == 0:
        return CapaCian
    elif layer_to_show == 1:
        return CapaMagenta
    elif layer_to_show == 2:
        return CapaYellow
