from odoo import fields, models, api, _
import feedparser as fp
import json
import newspaper
from newspaper import Article


class Medios(models.Model):
    _name = "wsf_noticias_medios"
    _description = "modelo para ingresar las páginas"

    medio = fields.Many2one('res.partner')
    pagina_web = fields.Char('Pagina Web:')
    pagina_rss = fields.Char('Pagina rss:')
    importancia = fields.Selection([('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')])
    pauta = fields.Float('Pauta')
    estado = fields.Selection([('on', 'ON'), ('off', 'OFF')])
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
        for rec in all_records:
            limite = 50

            datos = {}
            datos['Noticias'] = {}

            # Llamar al archivo JSON

            with open('paginas.json') as archivos_datos:
                paginas = json.load(archivos_datos)

            # Iterar por cada pagina de noticias

            contador = 1

            for pagina, valor in paginas.items():
                # Checar si hay un link rss en el json para darle prioridad
                if 'rss' in valor:
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
                        article['link'] = entrada.link
                        try:
                            contenido = Article(entrada.link)
                            contenido.download()
                            contenido.parse()
                        except Exception as e:
                            # Para evitar errores en caso de problemas de conexion
                            # En caso de error el programa seguira el ciclo e imprimira continuar
                            print(e)
                            print("continuando...")
                            continue
                        article['titulo'] = contenido.title
                        article['texto'] = contenido.text
                        newsPaper['articulos'].append(article)
                        print(contador, "Articulo descargado de", pagina, ", url: ", entrada.link)
                        contador = contador + 1

                else:
                    # El Else es para las paginas que no cuentan con un rss
                    # Se usa la libreria de newspaper para extraer articulos

                    print("Descargando articulos de: :  ", pagina)
                    hoja = newspaper.build(valor['link'], memoize_articles=False)
                    newsPaper = {
                        "pagina": pagina,
                        "link": valor['link'],
                        "articulos": []
                    }
                    contador = 0

                    # hoja.articles -> obtiene una lista con todos los artículos del portal que está visitando (escrapeando)
                    for contenido in hoja.articles:  # recorre cada uno de los artículos
                        if contador > limite:
                            break
                        try:
                            contenido.download()
                            contenido.parse()
                        except Exception as e:
                            print(e)
                            print("continuando...")
                            continue

                        # noticia concreta
                        article = {}

                        # article['fecha'] = datetime.datetime.now()
                        article['titulo'] = contenido.title
                        article['texto'] = contenido.text
                        article['link'] = contenido.url

                        # todo: ver como sacar la fecha. Estudiar el newspaper
                        # article['fecha_articulo']

                        # lista de artículos para este sitio
                        newsPaper['articulos'].append(article)

                        print(contador, "Articulo descargado de", pagina, " url: ", contenido.url)
                        contador = contador + 1
                        noneTypecontador = 0

                contador = 1
                datos['Noticias'][pagina] = newsPaper

            # Por ultimo todo se guarda en un archivo json
            try:
                with open('noticias.json', 'w', encoding='utf-8') as outfile:
                    json.dump(datos, outfile)
            except Exception as e:
                print(e)
