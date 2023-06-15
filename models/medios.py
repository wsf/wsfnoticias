from odoo import fields, models, api, _

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


