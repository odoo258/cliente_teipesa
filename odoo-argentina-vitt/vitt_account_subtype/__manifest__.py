# -*- coding: utf-8 -*-
{
    'name': "subtipo para diarios y pagos/recibos",

    'summary': """subtipo para diarios y pagos/recibos""",

    'description': """
        agrega subtipo para diarios y pagos/recibos y filtrar los diarios
    """,
    'author': "Moogah",
    'website': "http://www.Moogah.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['account_payment_group','account',],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'application': True,
}