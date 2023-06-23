from odoo import fields, models, api, _

class Reglas(models.Model):
    _name = "wsf_noticias_reglas"
    _description = "modelo para ingresar los criterios de busqueda de informacion"

    # medio = fields.Many2one('res.partner')
    nombre_regla = fields.Char('Nombre de la regla:')
    terminos_or = fields.Many2many('wsf_noticias_terminos',relation='wsf_noticias_terminos_or')
    terminos_and = fields.Many2many('wsf_noticias_terminos', relation='wsf_noticias_terminos_and')
    terminos_not = fields.Many2many('wsf_noticias_terminos',relation='wsf_noticias_terminos_not')
    estado = fields.Selection([('on', 'ON'), ('off', 'OFF')])
    fecha_desde = fields.Date('Fecha Desde:')
    fecha_hasta = fields.Date('Fecha Hasta:')
    mails = fields.Text("Mails para avisar")
    telegram  = fields.Text("URL Bot telegram")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s' % (rec.nombre_regla)))
        return result


class Terminos(models.Model):
    _name = "wsf_noticias_terminos"
    _description = "modelo para guardar terminos de busqueda"

    name = fields.Char('Termino')