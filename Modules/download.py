import urllib.request

def file(url, name):
    ext = '.jpg'
    if url.endswith('.webp'):
        ext = '.webp'
    elif url.endswith('.png'):
        ext = '.png'
    file = f"Downloads/{name}"
    route = file+ext
    r = urllib.request.urlopen(url)
    f = open(route, "wb")
    f.write(r.read())
    f.close()

    """
    ruta = f'Downloads/{name}.webp'
    # Crear un objeto Request con la URL y cualquier parámetro adicional necesario
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0'  # especificar el agente de usuario para evitar problemas de bloqueo
        }
    )

    # Descargar el archivo desde la URL y guardarlo localmente
    with urllib.request.urlopen(req) as response, open(ruta, 'wb') as out_file:
        out_file.write(response.read())
    """