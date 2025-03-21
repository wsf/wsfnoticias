import textblob
import requests
import datetime as datetime
import re

# https://api.telegram.org/botAAFfoTbrGSXwXm20KFPB/getUpdates
# https://api.telegram.org/bot6197272098:AAFfoTbrGSXwXm20KFPB-1B-rb1EHveCYBM/getUpdates





def limpiar_texto(texto):
    r = texto.replace("'","").replace('"',"")
    return r


def enviar_telegram(article,medio="Medio", chat_id = '-918982585',bot_token = '6197272098:AAFfoTbrGSXwXm20KFPB-1B-rb1EHveCYBM' ):

    try:
        # armo el texto a enviar con article:
        message = ""


        #message += str(article['medio'])
        message += "\n-- 🗞️ -- \n"
        message += medio
        message += "\n-- \n"
        message += article['titulo'].upper()
        message += "\n--\n"

        #message += article['tipo'].upper()

        """
        if article['tipo'].upper() == "NEGATIVA":
            message += " 🔴🔴🔴🔴🔴🔴"
        elif article['tipo'].upper() == "POSITIVA":
            message += " 🟢🟢🟢🟢🟢🟢"
        else:
            message += " 🟡🟡🟡🟡🟡🟡"
        """

        message += "\n\n"
        message += article['link']


        # Replace YOUR_BOT_TOKEN with your actual bot token
        #bot_token = '6197272098:AAFfoTbrGSXwXm20KFPB-1B-rb1EHveCYBM'

        # Replace YOUR_CHAT_ID with the chat ID you want to send the message to
        #chat_id = '1007231414'

        # The message you want to send
        #message = 'Hello, world!'

        # Make a POST request to the Telegram API to send the message
        response = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendMessage',
            data={
                'chat_id': chat_id,
                'text': message
            }
        )

        # Check if the request was successful
        if response.status_code == 200:
            print('Message sent successfully!')
        else:
            print('Failed to send message:', response.text)

    except Exception as e:
        print(str(e))


def enviar_telegram_estadistica(message, chat_id = '-900652227',bot_token = '6197272098:AAFfoTbrGSXwXm20KFPB-1B-rb1EHveCYBM' ):

    try:
        # Make a POST request to the Telegram API to send the message
        response = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendMessage',
            data={
                'chat_id': chat_id,
                'text': message
            }
        )

        # Check if the request was successful
        if response.status_code == 200:
            print('Message sent successfully!')
        else:
            print('Failed to send message:', response.text)

    except Exception as e:
        print(str(e))


def aplica_regla(titulo, cuerpo, copete,reglas):
    regla_nombre = set()
    telegram = []
    lista_condicionales = []
    log = ""

    # reglas
    for r in reglas:

        cumple_or, cumple_and, cumple_not = False, False, False

        # terminos or -------------------------------------------
        terminos = r.terminos_or

        lista_condicionales = []
        condi = False

        log += f"\n\n----------------------------------------------------------" \
               f"----------------------------------------------------------" \
               f"\n** Aplicando la regla: {r.nombre_regla.upper()} para el artículo con título: {titulo.upper()}:\n"
        for t in terminos:

            condi_titulo = t.name.upper() in titulo.upper()
            condi_cuerpo = t.name.upper() in cuerpo.upper()
            condi_copete = t.name.upper() in copete.upper()

            condi = condi_copete or condi_titulo or condi_cuerpo

            log += f"\n - Analiza regla OR con el termino {t.name.upper()}"

            if condi:
                #regla_nombre.add(r.nombre_regla)
                log += f"\n -- entra por regla or, por el termino {t.name.upper()}"
                cumple_or = True

        # si no hay terminos en or ->
        if not terminos:
            log += f"\n -- no hay terminos  or en la regla"
            cumple_or = True


        # terminos and  -------------------------------------------
        terminos = r.terminos_and

        cumple_and = True
        for t in terminos:

            condi_titulo = t.name.upper() in titulo.upper()
            condi_cuerpo = t.name.upper() in cuerpo.upper()
            condi_copete = t.name.upper() in copete.upper()

            condi = condi_copete or condi_titulo or condi_cuerpo

            log += f"\n - Analiza regla AND con el termino {t.name.upper()}"
            if not condi:
                # cualquiera que no cumpla el and
                log += f"\n -- no cumple en and  {t.name.upper()}"
                cumple_and = False
                break

        if cumple_and and terminos:
            #regla_nombre.add(r.nombre_regla)
            log += f"\n -- cumple en and  {t.name.upper()}"
            cumple_and = True

        if not terminos:
            log += f"\n -- no hay terminos and en la regla"
            cumple_and = True

        # terminos not  -------------------------------------------
        terminos = r.terminos_not

        lista_condicionales = []
        for t in terminos:

            condi_titulo = t.name.upper() not in titulo.upper()
            condi_cuerpo = t.name.upper() not in cuerpo.upper()
            condi_copete = t.name.upper() not in copete.upper()

            condi = condi_copete and condi_titulo and condi_cuerpo

            log += f"\n - Analiza regla NOT con el termino {t.name.upper()}"
            if condi:
                #regla_nombre.add(r.nombre_regla)
                log += f"\n -- cumple con not  {t.name.upper()}"
                cumple_not = True

        if not terminos:
            log += f"\n -- no hay terminos not en la regla"
            cumple_not = True


        # Verifico que se cumplan todos los tipo de condicionales
        if cumple_and and cumple_not and cumple_or:
            log += f"\n -- filtra !!!!!!!!!!!!!!!!!!  {t.name.upper()}"
            regla_nombre.add(r.nombre_regla)
            telegram.append(r.telegram)
        else:
            log += f"\n -- no filtra *************** "
            regla_nombre.add('set()')


    return (str(regla_nombre),log,telegram)

def filtra_url(article_link, url_medio2, url_medio):
    condi = True
    condi1 = article_link[0:len(url_medio2) + 1].replace("http://", "").replace("https://", "") == url_medio.replace(
        "http://", "").replace("https://", "")
    condi2 = "/rss" in article_link or "/feed" in article_link

    condi  =  condi and not condi2

    return condi

def sentimiento(texto):
    blob = textblob.TextBlob(texto)
    blob = blob.translate(from_lang='es',to='en')

    r = blob.sentiment.polarity
    if r < 0:
        sentiment = "negativa"
    elif r > 0:
        sentiment = "positiva"
    else:
        sentiment = "neutra"

    return sentiment

def entidades(texto):
    return ""
    try:
        entidades = textblob.TextBlob(texto).noun_phrases
        entidades = list(filter(lambda x: len(x) > 4, entidades))

        print(entidades)
    except:
        entidad = "-"
    return entidades

import string

def nube(text):
    # Convertir el texto a minúsculas y eliminar los caracteres no alfabéticos
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Dividir el texto en palabras y generar una lista de palabras únicas
    words = set(text.split())

    # Eliminar las palabras vacías de la lista de palabras únicas
    stopwords = {'va','tan','fue','era','san','ha', 'a', 'e', 'y', 'o', 'u','art','se','on','us','me','ve','le','da','ver','a', 'y', 'o', 'el', 'la', 'ante', 'cabo', 'con', 'contra', 'de', 'desde', 'para', 'por', 'según',
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
                 'parecer', 'resultar', 'permanecer', 'continuar',
                 'siempre', 'nunca', 'raramente', 'frecuentemente',
                 'sí', 'ciertamente', 'claro que sí',
                 'no', 'tampoco', 'jamás',
                 'quizás', 'tal vez', 'probablemente',
                 'rápidamente', 'lentamente', 'cuidadosamente',
                 'demasiado', 'bastante', 'suficientemente',
                 'arriba', 'abajo', 'cerca', 'lejos',
                 'que', 'quien', 'cuyo', 'cuyos', 'cuya', 'cuyas', 'donde', 'cuando', 'como',
                 'si', 'como', 'porque', 'aunque', 'mientras', 'cuando', 'donde', 'quien',
                 'ir', 'venir', 'hacer', 'decir', 'ver', 'sentir', 'pensar', 'creer', 'conocer', 'entender', 'querer',
                 'poder', 'deber',
                 'bailar', 'cantar', 'tocar', 'cocinar', 'leer', 'escribir', 'correr', 'nadar', 'jugar', 'mirar',
                 'escuchar','vi','te','le','me','mi','da','ex','uno','dos','tres'
                 }

    words = words - stopwords

    # Contar el número de veces que aparece cada palabra en el texto
    word_count = {}
    for word in words:
        count = text.count(word)
        if len(word) > 3 and count > 1:
            word_count[word] = count

    # ordernarlo:
    sorted_dict = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))

    # Devolver el diccionario con el recuento de palabras
    return str(sorted_dict)


import sqlite3


def telegram_norep_add_autoincrement():

    q = "ALTER TABLE norep ADD COLUMN fecha TEXT;"
    nombre = os.path.dirname(__file__) + '/telegram_norep.db'
    conexion = sqlite3.connect(nombre)
    cursor = conexion.cursor()
    cursor.execute(q)

    conexion.commit()
    pass


def telegram_norep_init():

    nombre = os.path.dirname(__file__) + '/telegram_norep.db'
    conexion = sqlite3.connect(nombre)
    cursor = conexion.cursor()

    # Creamos una tabla
    cursor.execute('''CREATE TABLE norep
                      (titulo TEXT KEY, link TEXT)''')

    # Insertamos algunos datos
    cursor.execute("INSERT INTO norep VALUES ('t1', 'l1')")
    cursor.execute("INSERT INTO norep VALUES ('t2', 'l2')")

    # Guardamos los cambios
    conexion.commit()


#telegram_norep_init()

def depurar_no_rep():
    yymm =  datetime.datetime.now().strftime('%Y%m')
    ano = yymm[0:4]
    mes = int(yymm[4:6]) - 1
    mes2 = int(yymm[4:6]) - 2

    yymm1 = ""
    yymm2 = ""

    print(yymm)
    nombre = os.path.dirname(__file__) + '/telegram_norep.db'
    conexion = sqlite3.connect(nombre)
    cursor = conexion.cursor()

    q = f"delete from norep where  fecha = '{yymm1}' or fecha = '{yymm2}'"
    cursor.execute(q)
    conexion.commit()


import os
def telegram_norep(titulo,link):

    yymm = datetime.datetime.now().strftime('%Y%m')

    nombre = os.path.dirname(__file__) + '/telegram_norep.db'
    conexion = sqlite3.connect(nombre)
    cursor = conexion.cursor()

    q = f"select titulo from norep where titulo = '{titulo}'"
    cursor.execute(q)
    resultados=cursor.fetchall()

    if resultados:

        return True
    else:
        q = f"INSERT INTO norep VALUES ('{titulo}','{link}','{yymm}')"
        cursor.execute(q)
        conexion.commit()

        return False


def telegram_listar():

    nombre = os.path.dirname(__file__) + '/telegram_norep.db'
    conexion = sqlite3.connect(nombre)
    cursor = conexion.cursor()
    q = "select fecha, titulo from norep"
    cursor.execute(q)
    resultados=cursor.fetchall()
    for r in resultados:
        print(r)

import sys

def main():

    try:
        parametro = sys.argv[1]
        fecha = sys.argv[2]

        if parametro == "borrar":

            nombre = os.path.dirname(__file__) + '/telegram_norep.db'
            conexion = sqlite3.connect(nombre)
            cursor = conexion.cursor()

            telegram_listar()


            q = f"delete from norep where fecha = '{fecha}'"
            cursor.execute(q)
            conexion.commit()
    except:
        pass



if __name__ == "__main__":
    #telegram_norep_add_autoincrement()
    #telegram_listar()
    #r =  sentimiento("Esta es una frase positiva y linda")
    #print(r)
    main()

depurar_no_rep()

#r  = telegram_norep('t1','l1')
#r2  = telegram_norep('t5','l5')
#print(r,r2)

