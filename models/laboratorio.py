from odoo import fields, models, api, _
from datetime import *
import pytz
IST = pytz.timezone('America/Argentina/Buenos_Aires')
import random

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

    def fun_ac(self,noti,a_c):
        # obtener la clase
        clase = "c1"

        if clase in a_c.keys():
            a_c[clase] = a_c[clase] + 1
        else:
            a_c[clase] = 1

    def fun_as(self,noti, a_s):

        r = ""

        if r == "positivo":
            a_s[0] = a_s[0] + 1
        elif r == "neutra":
            a_s[1] = a_s[1] + 1
        if r == "negativa":
            a_s[2] = a_s[2] + 1

        return a_s

    def fun_ae(self,noti,a_e):

        # aplicar analisis
        lista_entidades  = []

        for e in lista_entidades:
            a_e.add(e)
        return a_e


    def procesar2(self):
        condi = [('fecha_registro', '>=', self.fecha_desde), ('fecha_registro', '<=', self.fecha_hasta)]
        noticias = self.env['wsf_noticias_resultados'].search(condi)

        a_s = [10,33,5]
        a_c = {'clase1':1}
        a_e = set()

        for n in noticias:
            a_s = self.fun_as(n,a_s)
            a_c.append(self.fun_ac(n))
            a_e = self.fun_ae(n,a_e)

        # hacer promedio de los valores

        # armar el html para mostar los resultados que hay de todas las noticas en los: a_s, a_c, a_e




    def procesar_labo(self):
        condi = [('fecha_registro', '>=', self.fecha_desde), ('fecha_registro', '<=', self.fecha_hasta)]
        #noticias = self.env['wsf_noticias_resultados'].search(condi)



        noticias = self.env['wsf_noticias_resultados'].read_group(condi,
            ['fecha_registro', 'id:count_distinct'], ['fecha_registro'])

        titulos = "<table>"


        for n in noticias:

            #bloques = "🧱"*random.randint(1,10)

            bloques = "🧱" * n['fecha_registro_count']

            titulos += "<tr>"
            titulos += f"<td> {n['fecha_registro']} </td> <td> {bloques} </td>"
            titulos += "</tr>"

        titulos += "</table>"

        #titulos += self.grafica()



        self.analisis1 = titulos


    def grafica(self):

        grafica = """
        <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gráfico de barrasL</title>
 
    <style>
    .chart-wrap {
        --chart-width:420px;
        --grid-color:#aaa;
        --bar-color:#F16335;
        --bar-thickness:40px;
        --bar-rounded: 3px;
        --bar-spacing:10px;
 
        font-family:sans-serif;
        width:var(--chart-width);
    }
 
    .chart-wrap .title{
        font-weight:bold;
        padding:1.8em 0;
        text-align:center;
        white-space:nowrap;
    }
 
    /* cuando definimos el gráfico en horizontal, lo giramos 90 grados */
    .chart-wrap.horizontal .grid{
        transform:rotate(-90deg);
    }
 
    .chart-wrap.horizontal .bar::after{
        /* giramos las letras para horizontal*/
        transform: rotate(45deg);
        padding-top:0px;
        display: block;
    }
 
    .chart-wrap .grid{
        margin-left:50px;
        position:relative;
        padding:5px 0 5px 0;
        height:100%;
        width:100%;
        border-left:2px solid var(--grid-color);
    }
 
    /* posicionamos el % del gráfico*/
    .chart-wrap .grid::before{
        font-size:0.8em;
        font-weight:bold;
        content:'0%';
        position:absolute;
        left:-0.5em;
        top:-1.5em;
    }
    .chart-wrap .grid::after{
        font-size:0.8em;
        font-weight:bold;
        content:'100%';
        position:absolute;
        right:-1.5em;
        top:-1.5em;
    }
 
    /* giramos las valores de 0% y 100% para horizontal */
    .chart-wrap.horizontal .grid::before, .chart-wrap.horizontal .grid::after {
        transform: rotate(90deg);
    }
 
    .chart-wrap .bar {
        width: var(--bar-value);
        height:var(--bar-thickness);
        margin:var(--bar-spacing) 0;
        background-color:var(--bar-color);
        border-radius:0 var(--bar-rounded) var(--bar-rounded) 0;
    }
 
    .chart-wrap .bar:hover{
        opacity:0.7;
    }
 
    .chart-wrap .bar::after{
        content:attr(data-name);
        margin-left:100%;
        padding:10px;
        display:inline-block;
        white-space:nowrap;
    }
 
    </style>
</head>
<body>
 
<table>

    <tr>
        <td> 
            <div class="chart-wrap horizontal"> <!-- quitar el estilo "horizontal" para visualizar verticalmente -->
                <div class="title">Grafico con HTML y CSS que se puede visualizar horizontal o vertical</div>
               
                <div class="grid">
                    <div class="bar" style="--bar-value:10%;" data-name="Your Blog" title="Your Blog 85%"></div>
                    <div class="bar" style="--bar-value:20%;" data-name="Medium" title="Medium 23%"></div>
                    <div class="bar" style="--bar-value:30%;" data-name="Tumblr" title="Tumblr 7%"></div>
                    <div class="bar" style="--bar-value:38%;" data-name="Facebook" title="Facebook 38%"></div>
                    <div class="bar" style="--bar-value:35%;" data-name="YouTube" title="YouTube 35%"></div>
                    <div class="bar" style="--bar-value:30%;" data-name="LinkedIn" title="LinkedIn 30%"></div>
                    <div class="bar" style="--bar-value:5%;" data-name="Twitter" title="Twitter 5%"></div>
                    <div class="bar" style="--bar-value:20%;" data-name="Other" title="Other 20%"></div>
                    
                </div>
              </div>
              
        </td>


        <td> 
            <div class="chart-wrap horizontal"> <!-- quitar el estilo "horizontal" para visualizar verticalmente -->
                <div class="title">Grafico con HTML y CSS que se puede visualizar horizontal o vertical</div>
               
                <div class="grid">
                    <div class="bar" style="--bar-value:10%;" data-name="Your Blog" title="Your Blog 85%"></div>
                    <div class="bar" style="--bar-value:20%;" data-name="Medium" title="Medium 23%"></div>
                    <div class="bar" style="--bar-value:30%;" data-name="Tumblr" title="Tumblr 7%"></div>
                    <div class="bar" style="--bar-value:38%;" data-name="Facebook" title="Facebook 38%"></div>
                    <div class="bar" style="--bar-value:35%;" data-name="YouTube" title="YouTube 35%"></div>
                    <div class="bar" style="--bar-value:30%;" data-name="LinkedIn" title="LinkedIn 30%"></div>
                    <div class="bar" style="--bar-value:5%;" data-name="Twitter" title="Twitter 5%"></div>
                    <div class="bar" style="--bar-value:20%;" data-name="Other" title="Other 20%"></div>
                </div>
              </div>
              
        </td>



        <td> 
            <div class="chart-wrap horizontal"> <!-- quitar el estilo "horizontal" para visualizar verticalmente -->
                <div class="title">Grafico con HTML y CSS que se puede visualizar horizontal o vertical</div>
               
                <div class="grid">
                    <div class="bar" style="--bar-value:10%;" data-name="Your Blog" title="Your Blog 85%"></div>
                    <div class="bar" style="--bar-value:20%;" data-name="Medium" title="Medium 23%"></div>
                    <div class="bar" style="--bar-value:30%;" data-name="Tumblr" title="Tumblr 7%"></div>
                    <div class="bar" style="--bar-value:38%;" data-name="Facebook" title="Facebook 38%"></div>
                    <div class="bar" style="--bar-value:35%;" data-name="YouTube" title="YouTube 35%"></div>
                    <div class="bar" style="--bar-value:30%;" data-name="LinkedIn" title="LinkedIn 30%"></div>
                    <div class="bar" style="--bar-value:5%;" data-name="Twitter" title="Twitter 5%"></div>
                    <div class="bar" style="--bar-value:20%;" data-name="Other" title="Other 20%"></div>
                </div>
              </div>
              
        </td>

    </tr>




</table>

 
</body>
</html>
        """

        return grafica





