import textblob

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

def sentimiento(texto):
    blob = textblob.TextBlob(texto)
    blob = blob.translate("es")

    r = blob.sentiment.polarity
    if r < 0:
        sentiment = "negativa"
    elif r > 0:
        sentiment = "positiva"
    else:
        sentiment = "neutra"

    return sentiment

import string

def nube(text):
    # Convertir el texto a minúsculas y eliminar los caracteres no alfabéticos
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Dividir el texto en palabras y generar una lista de palabras únicas
    words = set(text.split())

    # Eliminar las palabras vacías de la lista de palabras únicas
    stopwords = {'a', 'y', 'o', 'el', 'la', 'ante', 'cabo', 'con', 'contra', 'de', 'desde', 'para', 'por', 'según',
                 'que','al','el','los','las','ellos','así','es','un','una','como','donde','esta','en','se','lo','ni','del','ese','de','si','no','estos','estas',
                 'hay','tuvo','poco','mucho','hace','es','los','las','tener','aquí',
                 'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
                 'yo', 'tú', 'él', 'ella', 'usted', 'nosotros', 'vosotros', 'ellos', 'ellas', 'ustedes',
                 'mi', 'tu', 'su', 'nuestro', 'vuestro', 'su',
                 'este', 'ese', 'aquel', 'esta', 'esa', 'aquella', 'esto', 'eso', 'aquello',
                 'alguien', 'nadie', 'algo', 'nada', 'alguno', 'ninguno', 'cualquiera', 'otro', 'varios', 'ambos',
                 'mismo', 'tantos', 'demás',
                 'a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'en', 'entre', 'hacia', 'hasta', 'para', 'por',
                 'según', 'sin', 'sobre', 'tras',
                 'y', 'e', 'ni', 'pero', 'sino', 'o', 'u', 'bien', 'ya', 'todavía', 'no obstante', 'sin embargo',
                 'porque', 'pues', 'así que', 'por lo tanto', 'luego', 'entonces',
                 'bien', 'mal', 'así', 'así así', 'regularmente', 'mejor', 'peor',
                 'ahora', 'antes', 'después', 'pronto', 'tarde', 'temprano',
                 'aquí', 'allí', 'cerca', 'lejos', 'encima', 'debajo', 'delante', 'detrás',
                 'mucho', 'poco', 'más', 'menos', 'suficiente',
                 'ser', 'estar', 'haber', 'tener',
                 'poder', 'deber', 'querer', 'saber',
                 'parecer', 'resultar', 'permanecer', 'continuar'
                 }

    words = words - stopwords

    # Contar el número de veces que aparece cada palabra en el texto
    word_count = {}
    for word in words:
        count = text.count(word)
        word_count[word] = count

    # ordernarlo:
    sorted_dict = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))

    # Devolver el diccionario con el recuento de palabras
    return str(sorted_dict)
