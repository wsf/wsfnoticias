# import xmlrpclib
import xmlrpc.client as xmlrpclib
import os
import datetime
import pytz

IST = pytz.timezone('America/Argentina/Buenos_Aires')

import feedparser as fp
import newspaper
from newspaper import Article

from tools.tools_xmlrpc import *


def conectar_xmlrpc(base):
    data = xmlrpc_config()

    # URL of the Odoo instance
    url = data['url']

    # Database name, username, and password

    if base=="":
        db_name = data['db_name']
    else:
        db_name = base

    username = data['username']
    password = data['password']

    # Connect to the Odoo instance
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db_name, username, password, {})

    # Create a new XML-RPC client instance
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    return models,db_name,uid,password


def _log(dato):
    if not "xxx" in dato:
        return

    nombre = os.path.dirname(__file__) + '/medio.log'
    log = open(nombre, 'a')
    dato = "- Log: " + str(datetime.datetime.now(IST)) + " ---> " + dato
    log.write(dato + '\n')
    log.close()


def scrap_noticias(importancia="todos", base="",  tipo="", pagina=""):

    models,db_name,uid,password = conectar_xmlrpc(base)

    telegram = ""

    filtro_importancia = []

    if importancia:
        filtro_importancia = [('importancia', '=', importancia)]
    else:
        filtro_importancia = []

    # all_records = self.env['wsf_noticias_medios'].search([('estado', '=', 'on'), ('importancia', '=', importancia)],
    #                                                      order="id asc")

    medios_ids = models.execute_kw(db_name, uid, password,
                                   'wsf_noticias_medios', 'search',
                                   [[('importancia', '=', importancia), ('estado', '=', 'on')]])

    medios = models.execute_kw(db_name, uid, password,
                               'wsf_noticias_medios', 'read', [medios_ids])

    # all_records = self.segmento(all_records, importancia)

    # reglas = self.env['wsf_noticias_reglas'].search([('estado', '=', 'on')])
    reglas_ids = models.execute_kw(db_name, uid, password,
                                   'wsf_noticias_reglas', 'search',
                                   [[('estado', '=', 'on')]])
    print(82)

    reglas = models.execute_kw(db_name, uid, password,
                               'wsf_noticias_reglas', 'read', [reglas_ids])

    try:
        search_ids = models.execute_kw(db_name, uid, password, 'wsf_noticias_resultados', 'search', [[]])
        models.execute_kw(db_name, uid, password,
                          'wsf_noticias_resultados', 'unlink', [search_ids])

        print(92)

    except Exception as e:
        print(e)


    try:

        contador22 = 0
        for rec in medios:


            print("\n\n**********\nTomando el medio: ", rec['medio'][1], " ",rec['importancia'],  "\n****\n")

            contador22 += 1
            print(contador22)

            mensaje = f"[xxx] Medio analidazo: {rec['medio'][1]} [xxx] {rec['importancia']} - Contador: {contador22}"
            _log(mensaje)

            if tipo == "prueba":
                if rec['pagina_web'] != pagina and rec['pagina_rss'] != pagina:
                    continue
                else:
                    prueba = "Comenzando a tomar información del portal a las: " + datetime.datetime.now(
                        IST).strftime(
                        '%Y/%m/%d %H:%M:%S') + "\n\n"

                    reglas = "Comenzando a visualizar las reglas: " + datetime.datetime.now(IST).strftime(
                        '%Y/%m/%d %H:%M:%S') + "\n\n"
            else:
                # if not (rec.estado == 'on' and rec.importancia == importancia):
                if not (rec['estado'] == 'on'):
                    continue

            _log(f"Tomando la página {rec['pagina_web']}")

            try:
                limite = rec['limite']

                datos = {}
                datos['Noticias'] = {}

                # Llamar al archivo JSON

                paginas = {
                    rec['medio'][0]: {
                        "rss": rec['pagina_rss'],
                        "link": rec['pagina_web']
                    }
                }
                lista_termninos = []
                contador = 1
                if rec['estado'] == 'on':

                    for pagina, valor in paginas.items():
                        # Checar si hay un link rss en el json para darle prioridad

                        if 'link' in valor and valor['link'] != False:

                            url_medio = valor['link']
                            if not "https://" in url_medio:
                                url_medio = "https://" + url_medio


                            hoja = newspaper.build(url_medio, memoize_articles=False)

                            newsPaper = {
                                "medio": pagina,
                                "link": valor['link'],
                                "articulos": []
                            }
                            contador = 1

                            if tipo == "prueba":
                                rec['prueba'] += f"Cantidad de artículos candidatos:  {len(hoja.articles)} \n"

                            # hoja.articles -> obtiene una lista con todos los artículos del portal que está visitando (escrapeando)
                            codigo = 0

                            for contenido in hoja.articles:  # recorre cada uno de los artículos

                                #print("\n\n**********\nContenido: ", str(contenido), "\n****\n")

                                if tipo == "prueba":
                                    limite = 10
                                if contador > limite:
                                    print("Sale - Sale - Sale")
                                    break
                                try:
                                    contenido.download()
                                    contenido.parse()


                                    #print("\n\n------------\nContenido download title: ", contenido.title, "\n")


                                except Exception as e:
                                    _log(f"Exception:  {str(e)}")
                                    pass
                                    print(e)

                                if tipo == "prueba":
                                    rec['prueba'] += f" \n -- Bajando artículo:  {str(contenido.url)} \n"

                                # en el lugar de texto, voy a pasar el uri de todos los links que tienen el key images y imgs

                                texto = tomar_literales_url(contenido)

                                texto += contenido.text


                                #r = aplica_regla(contenido.title, contenido.text, contenido.meta_description, reglas,models, db_name, uid, password)
                                r = aplica_regla(contenido.title, texto, contenido.meta_description, reglas,
                                                 models, db_name, uid, password)
                                lista_reglas = r[0]
                                telegram = r[2]

                                if tipo == "prueba":
                                    rec['reglas'] += r[1]

                                # _log(f" Aplicando regla \n  {r[1]}")

                                regla_nombre = lista_reglas.split(',')

                                if ('set' in (regla_nombre)[0] and len(
                                        list(
                                            regla_nombre)) == 1) and tipo != "prueba":  # si me devuelve set() es porque no aplicó regla

                                    # todo para publicidad: si no aplica es porque no hay publicidad detectada notificar
                                    valorar = "Revisar"
                                    #continue

                                else:
                                    valorar = "OK"

                                # noticia concreta
                                article = {}

                                #article['titulo'] = contenido.title.replace('“', "").replace("'", "").replace('"',
                                #                                                                              "").strip()

                                article['regla2'] = lista_reglas.replace("'set()'", "").replace("{", "").replace("}",
                                                                                                                 "").replace(
                                    "'", "").replace(",,", "")

                                if article['regla2'][0:2] == ', ':
                                    article['regla2'] = article['regla2'][2:]

                                try:

                                    encontrado = models.execute_kw(db_name, uid, password,
                                                                   'wsf_noticias_resultados', 'search',
                                                                   [[('link', '=', url_medio)]])


                                    # le pongo un false para que pase
                                    if encontrado and tipo != "prueba":

                                        if valorar == "OK":
                                            # lo borra

                                            models.execute_kw(db_name, uid, password,
                                                              'wsf_noticias_resultados', 'unlink',
                                                              [encontrado])
                                        else:

                                            continue

                                    else:
                                        # !!!!!! No está grabada
                                        article['medio'] = rec['medio'][0]
                                        medio = rec['medio'][1]

                                        #article['copete'] = contenido.meta_description.replace('"', '').replace("'",
                                        #                                                                       "").replace(
                                        #   '“', "")

                                        article['texto'] = contenido.text.replace('"', '').replace("'", "").replace('“',
                                                                                                                    "")

                                        try:
                                            #article['link'] = contenido.url.strip()
                                            #p ponga la ur del medio en lugar de la url de la noticia
                                            article['link'] = url_medio

                                        except Exception as e:
                                            _log(f"Exception 261:  {str(e)}")
                                            pass

                                        url_medio2 = url_medio.replace("https", "http")
                                        condi = filtra_url(article['link'], url_medio2, url_medio)

                                        if not condi:
                                            #print("XXXXXXXX Descartada por estar mal la ulr")

                                            continue

                                        article['fecha_registro'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                                        try:
                                            fecha2 = contenido.publish_date.strftime("%Y-%m-%d")
                                            article['fecha_hora'] = str(datetime.datetime.strptime(fecha2,"%Y-%m-%d"))

                                            # sila fecha del artículo es antigua (3 dias) lo descarta
                                            fecha_art = contenido.publish_date

                                            fecha_hoy = datetime.datetime.now(IST) - datetime.timedelta(days=3)

                                            # si la fecha del articulo tiene mas de 3 días no lo tomo
                                            if not fecha_art.strftime('%Y/%m/%d') >= fecha_hoy.strftime(
                                                    '%Y/%m/%d') and tipo != "prueba":
                                                #print("XXXXXXXX Descartada por fecha")

                                                #continue
                                                pass

                                        except Exception as e:
                                            try:
                                                print(str(e))
                                                pass
                                                # article['fecha_hora'] = datetime.datetime.strptime(fecha2,'%Y/%m/%d %H:%M:%S')
                                            except Exception as ee:
                                                _log(f"Exception 287:  {str(ee)}")
                                                pass
                                            print(str(e))
                                            pass

                                        #article['titulo'] = contenido.title.replace('"', '').replace("'", "").replace(
                                        #    '“',
                                        #    "").strip()

                                        #article['tipo'] = sentimiento(contenido.title)
                                        article['departamento'] = rec['departamento']
                                        article['valorar'] = valorar

                                        try:
                                            pass
                                            # article['nube'] = nube(contenido.text)[0:300]
                                            # article['entidades'] = entidades(contenido.text)

                                        except Exception as e:
                                            _log(f"Exception 302:  {str(e)}")

                                        if tipo == "prueba":

                                            rec['prueba'] += str(
                                                article) + f"\n\n  ------- Nuevo Artículo {contador}------- \n\n"

                                        else:

                                            # Guardo la noticia

                                            try:

                                                # **********************************************************
                                                # self.env['wsf_noticias_resultados'].sudo().create(article)
                                                # self.resultados.append(article)
                                                models.execute_kw(db_name, uid, password,
                                                                  'wsf_noticias_resultados', 'create', [article])
                                                #print("\n\n\n*** guardando ", str(article), "\n\n")
                                                # **********************************************************
                                            except Exception as e:
                                                medio += " -" + str(e)

                                            # medio += "\n\n- Reglas: " + article['regla2']
                                            codigo += 1
                                            medio += "\n- Código: " + str(codigo)

                                            # si es distinta de OK lo manda por telegram
                                            if valorar != 'OK':
                                                if telegram == []:
                                                    telegram = ['-981591564']
                                                enviar_telegram(article,medio,telegram)


                                            _log(f"****** Guardando \n {medio} \n {str(article)} ")

                                        contador = contador + 1

                                except Exception as e:
                                    _log(f"Exception 310:  {str(e)}")
                                    print(e)

                        contador = 1
                else:
                    pass
            except Exception as e:
                print(str(e))
                pass

    except Exception as e:
        print(e)
        pass

def tomar_literales_url(contenido):
    """
    images = contenido.images

    texto = ""

    for i in images:
        texto += i +  " "
        #print(i)

    images = contenido.imgs
    for i in images:
        texto += i + " "
        #print(i)
    """
    texto = contenido.html

    return texto

"""

scrap_noticias('alta')
scrap_noticias('media')
scrap_noticias('baja')
scrap_noticias('urgente')
scrap_noticias('cat1')
scrap_noticias('cat2')
scrap_noticias('cat3')
scrap_noticias('nuevo')
scrap_noticias('rss')
"""

scrap_noticias('alta',"")

import sys
if __name__ == "__main__":
    arg = sys.argv[1]

    try:
        base = sys.argv[2]
    except:
        base = ""


    print(arg, base)
    scrap_noticias(arg,base)
