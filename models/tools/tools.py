
def aplica_regla(titulo, cuerpo, copete,reglas):
    regla_nombre = set()
    lista_condicionales = []

    # reglas
    for r in reglas:

        cumple_or, cumple_and, cumple_not = False, False, False

        # terminos or -------------------------------------------
        terminos = r.terminos_or

        lista_condicionales = []
        condi = False


        for t in terminos:

            condi_titulo = t.name.upper() in titulo.upper()
            condi_cuerpo = t.name.upper() in cuerpo.upper()
            condi_copete = t.name.upper() in copete.upper()

            condi = condi_copete or condi_titulo or condi_cuerpo

            if condi:
                #regla_nombre.add(r.nombre_regla)
                cumple_or = True

        # si no hay terminos en or ->
        if not terminos:
            cumple_or = True


        # terminos and  -------------------------------------------
        terminos = r.terminos_and

        cumple_and = True
        for t in terminos:

            condi_titulo = t.name.upper() in titulo.upper()
            condi_cuerpo = t.name.upper() in cuerpo.upper()
            condi_copete = t.name.upper() in copete.upper()

            condi = condi_copete or condi_titulo or condi_cuerpo

            if not condi:
                # cualquiera que no cumpla el and
                cumple_and = False
                break

        if cumple_and and terminos:
            #regla_nombre.add(r.nombre_regla)
            cumple_and = True

        if not terminos:
            cumple_and = True

        # terminos not  -------------------------------------------
        terminos = r.terminos_not

        lista_condicionales = []
        for t in terminos:

            condi_titulo = t.name.upper() not in titulo.upper()
            condi_cuerpo = t.name.upper() not in cuerpo.upper()
            condi_copete = t.name.upper() not in copete.upper()

            condi = condi_copete and condi_titulo and condi_cuerpo

            if condi:
                #regla_nombre.add(r.nombre_regla)
                cumple_not = True

        if not terminos:
            cumple_not = True


        # Verifico que se cumplan todos los tipo de condicionales
        if cumple_and and cumple_not and cumple_or:
            regla_nombre.add(r.nombre_regla)
        else:
            regla_nombre = set()


    return str(regla_nombre)


def filtra_url(article_link, url_medio2, url_medio):
    condi = True
    condi1 = article_link[0:len(url_medio2) + 1].replace("http://", "").replace("https://", "") == url_medio.replace(
        "http://", "").replace("https://", "")
    condi2 = "/rss" in article_link or "/feed" in article_link

    condi  =  condi and not condi2

    return condi

