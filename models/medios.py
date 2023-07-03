from odoo import fields, models, api, _
import feedparser as fp
import json
import newspaper
from newspaper import Article
from datetime import *
import random
from .tools.tools import filtra_url, aplica_regla, sentimiento, nube, entidades, enviar_telegram, enviar_telegram_estadistica,telegram_norep
import os
import datetime
from odoo.http import request

def _log(dato):


    return
    nombre = os.path.dirname(__file__) + '/medio.log'
    log = open(nombre, 'a')
    dato = "- Log: " + str(datetime.datetime.now()) + " ---> " + dato
    log.write(dato + '\n')
    log.close()


wsf_noticias_norep = []
resultados = []
norepe2 = []

class Medios(models.Model):
    _name = "wsf_noticias_medios"
    _description = "modelo para ingresar las páginas"
    _order = "id desc"

    medio = fields.Many2one('res.partner', tracking=True)
    limite = fields.Integer('Limite')
    pagina_web = fields.Char('Pagina Web:' , tracking=True)
    pagina_rss = fields.Char('Pagina rss:', tracking=True)
    regla = fields.Many2one('wsf_noticias_reglas')
    importancia = fields.Selection([('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'),('prueba', 'Prueba'),('nuevo','Nuevo'),('cat1','Categoría #1'),('cat2','Categoría #2'),('cat3','Categoría #3')])
    pauta = fields.Float('Pauta')
    estado = fields.Selection([('on', 'ON'), ('off', 'OFF')], required=True)
    puntuacion = fields.Char('Puntuacion')
    comentario = fields.Text('Comentario', tracking=True)
    latitud = fields.Char('Latitud')
    longitud = fields.Char('Longitud')
    prueba = fields.Text('Prueba')
    reglas = fields.Text('Reglas')
    resultado1 = fields.Html(default='<h1> Labo1 </h1')
    resultado2 = fields.Html(default='<h1> Labo2 </h1')
    departamento = fields.Char('Departamento')



    def verificar_notep(self):
        # recorro resultados
        try:
            for r in norepe2:
                try:
                    titulo = r
                    condi = [('titulo','=',titulo)]
                    result = self.env['wsf_noticias_norep'].sudo().search(condi)
                    if not result:
                        jr = {}
                        jr['titulo']=r
                        self.env['wsf_noticias_norep'].sudo().create(jr)
                except Exception as e:
                    print(e)

        except Exception as e:
            print(str(e))



    def verificar_resultados(self):
        # recorro resultados
        try:
            for r in resultados:
                try:
                    link = r['link']
                    condi = [('link','=',link)]
                    result = self.env['wsf_noticias_resultados'].sudo().search(condi)
                    if not result:
                        self.env['wsf_noticias_resultados'].sudo().create(r)
                except Exception as e:
                    print(e)

        except Exception as e:
            print(str(e))


    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s' % (rec.medio.display_name)))
        return result

    def scrap_prueba(self):
        if self.pagina_web:
            self.scrap_noticias("todos","prueba",self.pagina_web)
        else:
            self.scrap_noticias("todos","prueba",self.pagina_rss)

    def scrap_importancia_prueba(self):
        self.scrap_noticias('prueba')

    @api.model
    def estadisticas_diaria(self):

        # filtar las noticias del día


        condi = [('fecha_registro', '>=', datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')),
                  ('fecha_registro', '<=', datetime.datetime.now().strftime('%Y-%m-%d 23:59:59'))]

        #rec = self.env['wsf_noticias_resultados'].search(condi)

        rec = self.env['wsf_noticias_resultados'].read_group(condi,
                                                                  ['regla2', 'id:count_distinct'],
                                                                  ['regla2'])
        mensaje = "\n📈 Estadística diaria 📈 \n"

        mensaje += "\n\n**Aplicación de reglas hoy**\n\n"

        for r in sorted(rec,key=lambda r:r['regla2_count'],reverse=True):

            mensaje += f"- 📏 [{r['regla2']}] se aplicó: [{r['regla2_count']}] veces \n"


        rec = self.env['wsf_noticias_resultados'].read_group(condi,
                                                                  ['medio', 'id:count_distinct'],
                                                                  ['medio'])

        mensaje += "\n\n**Medios alcanzados hoy**\n\n"
        for r in sorted(rec,key=lambda r:r['medio_count'],reverse=True):

            mensaje += f"- 📰 [{r['medio'][1]}] brindo noticias: [{r['medio_count']}] veces \n"

        enviar_telegram_estadistica(mensaje)



    @api.model
    def scrap_importancia_nuevo(self):
        self.scrap_noticias('nuevo')

    @api.model
    def scrap_importancia_cat1(self):
        self.scrap_noticias('cat1')
        self.verificar_resultados()


    @api.model
    def scrap_importancia_cat2(self):
        self.scrap_noticias('cat2')
        self.verificar_resultados()


    @api.model
    def scrap_importancia_baja(self):
        self.scrap_noticias('baja')
        self.verificar_resultados()


    @api.model
    def scrap_importancia_alta(self):
        self.scrap_noticias('alta')
        self.verificar_resultados()


    @api.model
    def scrap_importancia_media(self):
        self.scrap_noticias('media')
        self.verificar_resultados()


    @api.model
    def scrap_importancia_todos(self):
        self.scrap_noticias('todos')
        self.verificar_resultados()
        self.verificar_notep()

    @api.model
    def scrap_noticias(self, importancia="todos", tipo="", pagina=""):


        telegram = ""

        filtro_importancia = []

        if importancia == 'baja':
            filtro_importancia = [('importancia', '=', 'baja')]
        elif importancia == 'media':
            filtro_importancia = [('importancia', '=', 'media')]
        elif importancia == 'alta':
            filtro_importancia = [('importancia', '=', 'alta')]
        elif importancia == 'prueba':
            filtro_importancia = [('importancia', '=', 'prueba')]
        elif importancia == 'cat1':
            filtro_importancia = [('importancia', '=', 'cat1')]
        elif importancia == 'cat2':
            filtro_importancia = [('importancia', '=', 'cat2')]
        elif importancia == 'nuevo':
            filtro_importancia = [('importancia', '=', 'nuevo')]
        else:
            filtro_importancia = []

        all_records = self.env['wsf_noticias_medios'].search(filtro_importancia,order='medio asc')

        all_records_resultados = self.env['wsf_noticias_resultados'].search([])

        for rec in all_records:

            if tipo == "prueba":
                if  rec.pagina_web != pagina and  rec.pagina_rss != pagina:
                    continue
                else:
                    self.prueba = "Comenzando a tomar información del portal a las: " + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "\n\n"
                    self.reglas = "Comenzando a visualizar las reglas: " + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "\n\n"
            else:
                if not (rec.estado == 'on' and rec.importancia == importancia):
                    continue


            _log(f"Tomando la página {rec.pagina_web}")

            try:
                limite = rec.limite

                datos = {}
                datos['Noticias'] = {}

                # Llamar al archivo JSON

                paginas = {
                    rec.medio.id: {
                        "rss": rec.pagina_rss,
                        "link": rec.pagina_web
                    }
                }
                lista_termninos = []

                # las reglas se aplican para todos. No para un medio particular
                """
                for t in rec.regla.terminos_and:
                    lista_termninos.append(t.name)
                """
                # Iterar por cada pagina de noticias


                contador = 1
                if rec.estado == 'on':
                    for pagina, valor in paginas.items():
                        # Checar si hay un link rss en el json para darle prioridad
                        if 'rss' in valor and valor['rss'] != False:
                            v = fp.parse(valor['rss'])
                            print("Descargando articulos de: ",
                                  pagina)  # Se crea un diccionario con la palabra reservada newspaper jalando los datos de nuestro json
                            newsPaper = {
                                "pagina": pagina,
                                "link": valor['link'],
                                "articulos": []  # Se crea un elemento en blanco, donde se guardaran las noticias
                            }

                            codigo = 0
                            for entrada in v.entries:

                                if tipo=="prueba":
                                    limite = 50

                                if contador > limite:
                                    break
                                article = {}

                                # article['keywords'] = entrada
                                try:
                                    contenido = Article(entrada.link)
                                    contenido.download()
                                    contenido.parse()
                                except Exception as e:
                                    _log(f"Exception:  {str(e)}")

                                    print(e)
                                    continue

                                article['titulo'] = contenido.title.replace('“',"").replace("'","").replace('"',"").strip()

                                try:

                                    reglas = self.env['wsf_noticias_reglas'].search([('estado','=','on')])
                                    r = aplica_regla(contenido.title, contenido.text,
                                                                contenido.meta_description, reglas)
                                    lista_reglas = r[0]

                                    telegram = r[2]

                                    #_log(f" Aplicando regla \n  {r[1]}")

                                    if tipo  == "prueba":
                                        self.reglas += r[1]

                                    regla_nombre = lista_reglas.split(',')

                                    if ('set' in (regla_nombre)[0] and len(list(regla_nombre)) == 1) and tipo != "prueba":
                                        continue

                                    encontrado = self.env['wsf_noticias_resultados'].search(
                                        [('link', '=', contenido.url)])


                                    if encontrado and tipo != "prueba":
                                        _log(f"*** Noticia ya guadada {str(encontrado)}")
                                        continue
                                    else:
                                        medio = rec.medio.name
                                        article['medio'] = rec.medio.id
                                        article['copete'] = contenido.meta_description.contenido.text.replace('"','').replace("'","")  ##
                                        article['texto'] = contenido.text.contenido.text.replace('"','').replace("'","")
                                        article['link'] = contenido.url.strip()
                                        article['tipo'] = sentimiento(contenido.title.contenido.text.replace('"','').replace("'",""))
                                        article['departamento'] = rec.departamento

                                        try:
                                            article['nube'] = nube(contenido.text )[0:300]
                                            article['entidades'] = entidades(contenido.text )
                                        except Exception as e:
                                            _log(f"Exception:  {str(e)}")


                                        try:

                                            fecha2 = contenido.publish_date.strftime('%Y/%m/%d %H:%M:%S')
                                            article['fecha_hora'] = datetime.datetime.strptime(fecha2,'%Y/%m/%d %H:%M:%S')

                                            # sila fecha del artículo es antigua (3 dias) lo descarta
                                            fecha_art = contenido.publish_date

                                            fecha_hoy = datetime.datetime.now() - datetime.timedelta(days=3)

                                            # si la fecha del articulo tiene mas de 3 días no lo tomo
                                            if not fecha_art.strftime('%Y/%m/%d') >=  fecha_hoy.strftime('%Y/%m/%d') and tipo != "prueba":
                                                continue

                                        except Exception as e:
                                            try:
                                                article['fecha_hora'] = datetime.datetime.strptime(fecha2,'%Y/%m/%d %H:%M:%S')
                                            except Exception as e:
                                                _log(f"Exception: 208  {str(e)}")
                                                pass
                                            print(str(e))
                                            pass

                                        article['regla2'] = lista_reglas.replace("'set()'","").replace("{","").replace("}","").replace("'","").replace(",,",",")
                                        if article['regla2'][0:2] == ', ':
                                            article['regla2'] = article['regla2'][2:]


                                        if tipo == "prueba":
                                            self.prueba += str(article) + f"\n\n  ------- Nuevo Artículo {contador}------ \n\n"

                                        else:

                                            # Gruardo la Noticia
                                            _log(f"Guardando {str(article)}")

                                            all_records_resultados.sudo().create(article)
                                            resultados.appendarticle(article)

                                            medio += "\n- Reglas: " + article['regla2']
                                            codigo += 1
                                            medio += "\n- Código: " + str(codigo)

                                            notele = 0

                                            jnorep = []
                                            for tele in telegram:
                                                if tele:
                                                    if not telegram_norep(article['titulo'],article['link']):
                                                        enviar_telegram(article, medio, tele)
                                                else:
                                                    notele += 1
                                            if notele > 0:
                                                if not telegram_norep(article['titulo'], article['link']):
                                                    enviar_telegram(article, medio, tele)


                                        contador = contador + 1

                                except Exception as e:
                                    _log(f"Exception:  {str(e)}")
                                    print(e)

                        if 'link' in valor and valor['link'] != False:

                            url_medio = valor['link']
                            hoja = newspaper.build(url_medio, memoize_articles=False)

                            newsPaper = {
                                "medio": pagina,
                                "link": valor['link'],
                                "articulos": []
                            }
                            contador = 1

                            if tipo == "prueba":
                                self.prueba += f"Cantidad de artículos candidatos:  {len(hoja.articles)} \n"

                            # hoja.articles -> obtiene una lista con todos los artículos del portal que está visitando (escrapeando)
                            codigo = 0
                            for contenido in hoja.articles:  # recorre cada uno de los artículos

                                if tipo  == "prueba":
                                    limite = 50
                                if contador > limite:
                                    break
                                try:
                                    contenido.download()
                                    contenido.parse()

                                except Exception as e:
                                    _log(f"Exception:  {str(e)}")
                                    continue
                                    print(e)

                                if tipo == "prueba":
                                    self.prueba += f" \n -- Bajando artículo:  {str(contenido.url)} \n"

                                reglas = self.env['wsf_noticias_reglas'].search([('estado','=','on')])

                                r =  aplica_regla(contenido.title,contenido.text,contenido.meta_description, reglas)

                                lista_reglas = r[0]

                                telegram = r[2]

                                if tipo == "prueba":
                                    self.reglas += r[1]

                                #_log(f" Aplicando regla \n  {r[1]}")

                                regla_nombre = lista_reglas.split(',')

                                if ('set' in (regla_nombre)[0]  and  len(list(regla_nombre)) == 1) and tipo != "prueba":  # si me devuelve set() es porque no aplicó regla
                                    continue

                                # noticia concreta
                                article = {}
                                article['titulo'] = contenido.title.replace('“',"").replace("'","").replace('"',"").strip()
                                print(contenido.title)
                                article['regla2'] = lista_reglas.replace("'set()'", "").replace("{", "").replace("}",
                                                                                                                 "").replace(
                                    "'", "").replace(",,","")

                                if article['regla2'][0:2] == ', ':
                                    article['regla2'] = article['regla2'][2:]

                                try:
                                    encontrado = self.env['wsf_noticias_resultados'].search(
                                        [('link', '=', contenido.url)])

                                    print(contenido.text)

                                    if encontrado and tipo !="prueba":
                                        _log(f"*** Noticia ya guadada {str(encontrado)}")
                                        continue
                                    else:
                                        article['medio'] = rec.medio.id
                                        medio = rec.medio.name

                                        article['copete'] = contenido.meta_description.replace('"','').replace("'","").replace('“',"")
                                        article['texto'] = contenido.text.replace('"','').replace("'","").replace('“',"")

                                        try:
                                            article['link'] = contenido.url.strip()

                                        except Exception as e:
                                            _log(f"Exception 261:  {str(e)}")
                                            pass

                                        url_medio2 = url_medio.replace("https","http")
                                        condi = filtra_url(article['link'],url_medio2,url_medio)


                                        if not condi:
                                            continue
                                        try:
                                            fecha2 = contenido.publish_date.strftime('%Y/%m/%d %H:%M:%S')
                                            article['fecha_hora'] = datetime.datetime.strptime(fecha2,
                                                                                      '%Y/%m/%d %H:%M:%S')

                                            # sila fecha del artículo es antigua (3 dias) lo descarta
                                            fecha_art = contenido.publish_date

                                            fecha_hoy = datetime.datetime.now() - datetime.timedelta(days=3)

                                            # si la fecha del articulo tiene mas de 3 días no lo tomo
                                            if not fecha_art.strftime('%Y/%m/%d') >=  fecha_hoy.strftime('%Y/%m/%d') and tipo != "prueba":
                                                continue

                                        except Exception as e:
                                            try:
                                                article['fecha_hora'] = datetime.datetime.strptime(fecha2,'%Y/%m/%d %H:%M:%S')
                                            except Exception as ee:
                                                _log(f"Exception 287:  {str(ee)}")
                                                pass
                                            print(str(e))
                                            pass

                                        article['titulo'] = str(codigo+1) + " - " +  contenido.title.replace('"','').replace("'","").replace('“',"").strip()

                                        #article['tipo'] = random.choice(['positiva','negativa','neutra','neutra'])
                                        article['tipo'] = sentimiento(contenido.title)
                                        article['departamento'] = rec.departamento

                                        try:
                                            article['nube'] = nube(contenido.text )[0:300]
                                            article['entidades'] = entidades(contenido.text )
                                        except Exception as e:
                                            _log(f"Exception 302:  {str(e)}")

                                        if tipo == "prueba":

                                            self.prueba += str(article)+ f"\n\n  ------- Nuevo Artículo {contador}------- \n\n"

                                        else:

                                            # Guardo la noticia


                                            try:

                                                self.env['wsf_noticias_resultados'].sudo().create(article)
                                                resultados.append(article)

                                                # verifico que se haya grabado
                                                condi = [('link','=',article['link'])]

                                                grabado = self.env['wsf_noticias_resultados'].sudo().search(condi)

                                                if not grabado:

                                                    article2 ={}

                                                    article2['medio'] = article['medio']
                                                    article2['link']=article['link']
                                                    article2['departamento'] = article['departamento']
                                                    article2['tipo'] = article['tipo']


                                                    self.env['wsf_noticias_resultados'].sudo().create(article2)
                                                else:
                                                    # hago una marca en el telegram cuando no grabó
                                                    medio += " ###"

                                            except Exception as e:
                                                medio += " -" + str(e)

                                            print(article['texto'])

                                            medio += "\n\n- Reglas: " + article['regla2']
                                            codigo += 1
                                            medio += "\n- Código: " + str(codigo)

                                            # verifico que se haya grabado
                                            condi = [('titulo', '=', article['titulo'])]

                                            grabado = self.env['wsf_noticias_norep'].sudo().search(condi)
                                            grabado2 =  article['titulo'] in wsf_noticias_norep

                                            if not (grabado or grabado2):
                                                norepe = {}
                                                norepe['titulo']=article['titulo']

                                                self.env['wsf_noticias_norep'].sudo().create(norepe)
                                                wsf_noticias_norep.append(article['titulo'])

                                                notele = 0

                                                jnorep = []

                                                for tele in telegram:
                                                    if tele:
                                                         if not telegram_norep(article['titulo'], article['link']):
                                                            enviar_telegram(article, medio, tele)
                                                    else:
                                                        notele += 1
                                                if notele > 0:
                                                    if not telegram_norep(article['titulo'], article['link']):
                                                        enviar_telegram(article, medio, tele)


                                            else:
                                                # encontró noticias repetidas
                                                pass

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