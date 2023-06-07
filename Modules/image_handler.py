import os
from PIL import Image

def convert_to_jpg(title):
    ruta = f"Downloads/{title}"
    try:
        with Image.open(ruta + '.webp') as im:
            im.convert("RGB").save(ruta + '.jpg')
        os.remove(ruta + '.webp')
    except Exception as e:
        print('[Error al intentar transformar la foto], más informacion abajo')

def ajustar_resolucion(ancho_original, alto_original):
    resolucion_maxima = 320
    # Calcular la proporción de aspecto de la imagen original
    proporcion_original = ancho_original / alto_original

    # Calcular el ancho y la altura de la imagen en la nueva resolución
    if proporcion_original >= 1:
        # La imagen es horizontal
        ancho_nuevo = resolucion_maxima
        alto_nuevo = int(ancho_nuevo / proporcion_original)
    else:
        # La imagen es vertical
        alto_nuevo = resolucion_maxima
        ancho_nuevo = int(alto_nuevo * proporcion_original)

    # Devolver la nueva resolución
    return (ancho_nuevo, alto_nuevo)

def thumbnail_compatible(title):
    """
    image = Image.open(f'Downloads/{title}.jpg')
    new_image = image.resize((320, 180))
    new_image.save(f'Downloads/{title}.jpg')
    """
    image = Image.open(f'Downloads/{title}.jpg')
    original_width = image.width
    original_height = image.height
    aspect_ratio = original_width / original_height
    # Verificamos si el ancho o la altura de la imagen original excede el tamaño máximo
    if original_width > 320:
        new_width = 320
        new_height = int(320 / aspect_ratio)
    elif original_height > 320:
        new_width = int(320 * aspect_ratio)
        new_height = 320
    else:
        new_width = original_width
        new_height = original_height
    new_image = image.resize((new_width, new_height))
    new_image.save(f'Downloads/{title}.jpg')