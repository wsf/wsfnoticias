# -*- coding: utf-8 -*-
{

    'name': 'wsf_noticias',
    'version': '1',
    'summary': 'WSF Noticias',
    'sequence': -101,
    'description': """WSF Noticias""",
    'author': 'MAN Group 2 ',
    'maintainer': 'MAN Group 2',
    'website': 'https://www.facebook.com/wsfnet',
    'license': 'AGPL-3',

    'depends': ['base','contacts'],

    'data': [
        'views/resultados.xml',
        'data/cron.xml',
        'views/medios.xml',
        'views/reglas.xml',
        'views/laboratorio.xml',
        'views/log.xml',
        'views/norep.xml',
        'views/secuencia.xml',
        'views/categorias.xml',
        'views/mapa.xml',
        'security/noticias_security.xml',
        'security/ir.model.access.csv'



    ],
    'demo': [],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
