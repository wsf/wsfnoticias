from odoo import fields, models, api, _
from datetime import *
import pytz
IST = pytz.timezone('America/Argentina/Buenos_Aires')

class Resultados(models.Model):
    _name = "wsf_noticias_laboratorio"
    _description = "laboratorio"
    _order = "fecha_registro desc"

    fecha_registro = fields.Datetime('Fecha registro',compute='compute_fecha_registro', store=True)
    nombre= fields.Char("Nombre")
    fecha_desde = fields.Datetime('Fecha Hasta')
    fecha_hasta = fields.Datetime('Fecha Desde')
    nube= fields.Char("Nube")
    clasificador = fields.Text("Clasificador")


    analisis1 = fields.Html()
    analisis2 = fields.Html()
    analisis3 = fields.Html()
    analisis4 = fields.Html()
    analisis5 = fields.Html()
    analisis6 = fields.Html()
    analisis7 = fields.Html()
    analisis8 = fields.Html()
    analisis9 = fields.Html()

    @api.depends('fecha_desde')
    def compute_fecha_registro(self):
        for rec in self:
            fecha = datetime.now(IST).strftime('%Y/%m/%d %H:%M:%S')
            rec.fecha_registro = datetime.strptime(fecha, '%Y/%m/%d %H:%M:%S')