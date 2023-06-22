import base64
from odoo import fields, models, api, _
import os

class Reglas(models.Model):
    _name = "wsf_noticias_log"
    _description = "modelo para ingresar los criterios de busqueda de informacion"


    text_file = fields.Binary(string='Archivo Log', default="medio.log")
    html_field = fields.Html(string='Detalle Log')

    @api.onchange('text_file')
    def _onchange_text_file(self):
        dirname = os.path.dirname(__file__)
        f = open(dirname+"/medio.log","r")
        ff = f.readlines()

        ll = ""
        for l in ff:
            if "Toma" in l:
                ll += f"<b> {l} </b> <br></br> <br></br> "
            else:
                ll += f"<a> {l} </a>  <br></br>  "

        cont = 0
        llista = []
        #for li in file_lines:

        if self.text_file:
            self.html_field = ll