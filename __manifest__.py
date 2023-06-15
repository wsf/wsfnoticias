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
        'data/cron.xml',
        'views/medios.xml',
        'views/resultados.xml',
        'views/reglas.xml',

    ],
    'demo': [],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
