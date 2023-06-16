from odoo import fields, models, api, _

class Resultados(models.Model):
    _name = "wsf_noticias_resultados"
    _description = "modelo para guardar los resultados"
    _order = "id desc"

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
