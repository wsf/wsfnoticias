from odoo import fields, models, api, _
from datetime import *
import pytz
IST = pytz.timezone('America/Argentina/Buenos_Aires')
from .tools.tools import enviar_telegram


class Norep(models.Model):
    _name = "wsf_noticias_norep"
    _description = "guarda registro para no repetir"
    _order = "fecha_registro desc"
    fecha_registro = fields.Datetime('Fecha registro',compute='compute_fecha_registro', store=True)
    link = fields.Char()
    titulo = fields.Char()


    @api.depends('link')
    def compute_fecha_registro(self):
        for rec in self:
            fecha = (datetime.now(IST) + datetime.timedelta(hours=3)).strftime('%Y/%m/%d %H:%M:%S')
            rec.fecha_registro = datetime.strptime(fecha, '%Y/%m/%d %H:%M:%S')




class Resultados(models.Model):
    _name = "wsf_noticias_resultados"
    _description = "modelo para guardar los resultados"
    _order = "fecha_registro desc"

    medio = fields.Many2one('res.partner')
    regla = fields.Many2one('wsf_noticias_reglas')
    fecha_hora = fields.Datetime('Fecha y Hora')
    titulo = fields.Char('Título')
    link = fields.Char('Link')
    copete = fields.Char('Copete')
    texto = fields.Text('Texto')
    tipo = fields.Selection([('positiva', "Pos"), ('negativa', 'Neg'), ('neutra', '???')])
    latitud = fields.Integer('Latitud')
    longitud = fields.Integer('Longitud')
    localidad = fields.Char('Localidad')
    departamento = fields.Char('Departamento')
    fecha_registro = fields.Datetime('Fecha registro',compute='compute_fecha_registro', store=True)
    dias = fields.Date('Día', compute='compute_day', store=True)
    hora = fields.Float('Hora', compute='compute_hour', store=True)
    regla2 = fields.Char('Reglas Aplicadas')
    valorar =  fields.Char('Valorar')
    nube = fields.Char('Nube')
    clasificacion = fields.Char('Clasificacion')
    entidades = fields.Char('Entidades')
    _sql_constraints = [
            ('link_uniq', 'UNIQUE (link)', 'Un solo link!'),
        ]

    # dias_hora = fields.Char('Dias_Hora', compute='dias_hora_agrupacion',store=True)


    @api.constrains('valorar')
    def _check_date_end(self):
       article2 = {}
       for record in self:
           if record.valorar == 'alertar':
               article2['titulo'] = record.titulo
               article2['link'] = record.link
               article2['tipo'] = record.tipo
               medio2 = record.medio.name

               enviar_telegram(article2,medio2,'-944811763')

           if  record.valorar == 'valorar':
                article2['titulo'] = record.titulo
                article2['link'] = record.link
                article2['tipo'] = record.tipo
                medio2 = record.medio.name

                enviar_telegram(article2, medio2, '-926479407')


    def remove_duplicate_record(self):
            model = self.env['wsf_noticias_resultados']
            records = model.read_group([],['link'], groupby=['link'])
            for r in records:

                if r['link_count'] > 1:
                   condi = [('link','=',r['link'])]
                   rr = self.env['wsf_noticias_resultados'].search(condi)[1:]
                   l  = [rrr.id for rrr in rr]
                   self.env['wsf_noticias_resultados'].search([('id', 'in', l)]).unlink()


    @api.depends('fecha_hora')
    def compute_day(self):
        for rec in self:
            if rec.fecha_hora:
                dia = rec.fecha_hora.strftime('%d-%m-%Y')
                rec.dias = datetime.strptime(dia, '%d-%m-%Y')

    @api.depends('fecha_hora')
    def compute_hour(self):
        for rec in self:
            if rec.fecha_hora:
                hora = rec.fecha_hora - timedelta(hours=3)
                rec.hora = hora.strftime('%H')

    @api.depends('fecha_hora')
    def compute_fecha_registro(self):
        for rec in self:
            fecha = (datetime.now(IST) + datetime.timedelta(hours=3)).strftime('%Y/%m/%d %H:%M:%S')

            rec.fecha_registro = datetime.strptime(fecha, '%Y/%m/%d %H:%M:%S')





    def set_alertar(self):
        for rec in self:
            rec.valorar = "alertar"


    def set_negativa(self):
        for rec in self:
            rec.valorar = "negativa"

    def set_positiva(self):
        for rec in self:
            rec.valorar = "positiva"

    def set_valorar(self):
        for rec in self:
            rec.valorar = "valorar"

    def set_archivar(self):
        for rec in self:
            rec.valorar = "archivar"

    # @api.depends('fecha_hora')
    # def dias_hora_agrupacion(self):
    #     for rec in self:
    #         rec.dias_hora = [rec.dias,rec.hora]

