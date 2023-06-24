from odoo import fields, models, api, _
from datetime import *
import pytz
IST = pytz.timezone('America/Argentina/Buenos_Aires')

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
    tipo = fields.Selection([('positiva', 'Positiva'), ('negativa', 'Negativa'), ('neutra', 'Neutra')])
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

    # dias_hora = fields.Char('Dias_Hora', compute='dias_hora_agrupacion',store=True)


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
            fecha = datetime.now(IST).strftime('%Y/%m/%d %H:%M:%S')
            rec.fecha_registro = datetime.strptime(fecha, '%Y/%m/%d %H:%M:%S')


    def set_marcar(self):
        for rec in self:
            rec.valorar = "valorar"

    def set_defender(self):
        for rec in self:
            rec.valorar = "defender"

    def set_contraatacar(self):
        for rec in self:
            rec.valorar = "contraatacar"

    def set_atacar(self):
        for rec in self:
            rec.valorar = "atacar"

    def set_diluir(self):
        for rec in self:
            rec.valorar = "diluir"

    # @api.depends('fecha_hora')
    # def dias_hora_agrupacion(self):
    #     for rec in self:
    #         rec.dias_hora = [rec.dias,rec.hora]

