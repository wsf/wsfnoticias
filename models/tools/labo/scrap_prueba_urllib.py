


def tomar_literales_url(contenido=None):
    import urllib.request


    #url = contenido.source_url
    url = "https://www.rosario3.com/"

    with urllib.request.urlopen(url) as response:
        html_completo = response.read().decode('utf-8')

    # seguir con bs4 analizando html_completo

    return html_completo

tomar_literales_url()