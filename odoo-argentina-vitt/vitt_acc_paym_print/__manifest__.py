# -*- coding: utf-8 -*-
{
    'name': "impresion de pagos y recibos",

    'summary': """Localizacion impresion de pagos y recibos""",

    'description': """
        impresion de pagos y recibos
    """,
    'author': "Moogah",
    'website': "http://www.Moogah.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'account_payment_group',
        'account_check',
        'vitt_val2words',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [],
    'application': True,
}