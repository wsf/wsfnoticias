def aplica_regla(titulo, cuerpo, copete,reglas):
    regla_nombre = set()


    for r in reglas:
        terminos = r.terminos_or

        for t in terminos:

            condi_titulo = t.name in titulo
            condi_cuerpo = t.name in cuerpo
            condi_copete = t.name in copete

            condi = condi_copete or condi_titulo or condi_cuerpo

            if condi:
                regla_nombre.add(r.nombre_regla)

    return str(regla_nombre)


def filtra_url(article_link, url_medio2, url_medio):
    condi = True
    condi1 = article_link[0:len(url_medio2) + 1].replace("http://", "").replace("https://", "") == url_medio.replace(
        "http://", "").replace("https://", "")
    condi2 = "/rss" in article_link or "/feed" in article_link

    condi  =  condi and not condi2

    return condi