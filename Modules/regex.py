import re

def get_nombre_ext(n_file):
    return re.search(r"[^/\\]*$", n_file).group()

def get_nombre(n_file):
    return re.search(r"[^/\\]*?(?=\.\w+$)", n_file).group()
