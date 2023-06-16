from odoo import fields, models, api, _
import feedparser as fp
import json
import newspaper
from newspaper import Article
from datetime import *

class Medios(models.Model):
    _name = "wsf_noticias_medios"
    _description = "modelo para ingresar las páginas"
    _order = "id desc"

    medio = fields.Many2one('res.partner')
    limite = fields.Integer('Limite')
    pagina_web = fields.Char('Pagina Web:')
    pagina_rss = fields.Char('Pagina rss:')
    regla = fields.Many2one('wsf_noticias_reglas')
    importancia = fields.Selection([('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')])
    pauta = fields.Float('Pauta')
    estado = fields.Selection([('on', 'ON'), ('off', 'OFF')], required=True)
    puntuacion = fields.Char('Puntuacion')
    comentario = fields.Text('Comentario')
    latitud = fields.Char('Latitud')
    longitud = fields.Char('Longitud')

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s' % (rec.medio.display_name)))
        return result

    @api.model
    def scrap_noticias(self):
        all_records = self.env['wsf_noticias_medios'].search([])
        all_records_resultados = self.env['wsf_noticias_resultados'].search([])

        for rec in all_records:
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
            for t in rec.regla.terminos_and:
                lista_termninos.append(t.name)
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
                        for entrada in v.entries:

                            if contador > limite:
                                break
                            article = {}

                            # article['keywords'] = entrada
                            try:
                                contenido = Article(entrada.link)
                                contenido.download()
                                contenido.parse()
                            except Exception as e:
                                print(e)
                                continue

                            article['titulo'] = contenido.title

                            try:
                                encontrado = self.env['wsf_noticias_resultados'].search(
                                    [('titulo', '=', article['titulo'])])
                                if encontrado:
                                    pass
                                else:
                                    article['medio'] = rec.medio.id
                                    article['copete'] = contenido.meta_description  ##
                                    article['texto'] = contenido.text
                                    article['link'] = contenido.url
                                    fecha = contenido.publish_date.strftime('%Y/%m/%d %H:%M:%S')
                                    article['fecha_hora'] = datetime.strptime(fecha, '%Y/%m/%d %H:%M:%S')

                                    all_records_resultados.create(article)
                                    contador = contador + 1

                            except Exception as e:
                                print(e)

                    else:

                        hoja = newspaper.build(valor['link'], memoize_articles=False)
                        newsPaper = {
                            "medio": pagina,
                            "link": valor['link'],
                            "articulos": []
                        }
                        contador = 1

                        # hoja.articles -> obtiene una lista con todos los artículos del portal que está visitando (escrapeando)
                        for contenido in hoja.articles:  # recorre cada uno de los artículos
                            if contador > limite:
                                break
                            try:
                                contenido.download()
                                contenido.parse()
                            except Exception as e:
                                print(e)
                                continue

                            # noticia concreta
                            article = {}
                            article['titulo'] = contenido.title

                            if lista_termninos:
                                # if lista_termninos[0] in contenido.text and lista_termninos[1] in contenido.text:
                                if lista_termninos[0] in contenido.text:
                                    try:
                                        encontrado = self.env['wsf_noticias_resultados'].search(
                                            [('titulo', '=', article['titulo'])])
                                        if encontrado:
                                            pass
                                        else:
                                            article['medio'] = rec.medio.id
                                            article['copete'] = contenido.meta_description ##
                                            article['texto'] = contenido.text
                                            article['link'] = contenido.url
                                            fecha2 = contenido.publish_date.strftime('%Y/%m/%d %H:%M:%S')
                                            article['fecha_hora'] = datetime.strptime(fecha2, '%Y/%m/%d %H:%M:%S')
                                            article['regla'] = rec.regla.id

                                            all_records_resultados.create(article)
                                            contador = contador + 1

                                    except Exception as e:
                                        print(e)

                    contador = 1
            else:
                pass