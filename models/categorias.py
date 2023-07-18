from odoo import fields, models, api, _

class Categorias(models.Model):
    _name = "wsf_noticias_categorias"
    _description = "modelo para categorias del clasificador"

    # medio = fields.Many2one('res.partner')
    name  = fields.Char('Categoria')
    estado = fields.Selection([('positiva', 'Positiva'), ('neutra', 'Neutra'), ('negativa', 'Negativa')])
    peso  = fields.Integer("Peso")
    descripcion = fields.Char('Descripción')
