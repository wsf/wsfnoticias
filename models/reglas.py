from odoo import fields, models, api, _

class Reglas(models.Model):
    _name = "wsf_noticias_reglas"
    _description = "modelo para ingresar los criterios de busqueda de informacion"

    medio = fields.Many2one('res.partner')
    nombre_regla = fields.Char('Nombre de la regla:')
    terminos_or = fields.Char('Terminos Or')
    terminos_and = fields.Char('Terminos And')
    terminos_not = fields.Char('Terminos Not')
    estado = fields.Selection([('on', 'ON'), ('off', 'OFF')])
    fecha_desde = fields.Date('Fecha Desde:')
    fecha_hasta = fields.Date('Fecha Hasta:')


