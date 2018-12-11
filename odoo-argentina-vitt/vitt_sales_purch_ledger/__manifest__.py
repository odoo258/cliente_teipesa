# -*- coding: utf-8 -*-
{
    'name': "cuentas por pagar/cobrar",

    'summary': """Libros cuentas por pagar/cobrar""",

    'description': """
        Reportes para Cuentas por pagar/cobrar del modulo ocontabilidad
    """,

    'author': "Moogah",
    'website': "http://www.Moogah.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account',
     ],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/templatessl.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'application': True,
}