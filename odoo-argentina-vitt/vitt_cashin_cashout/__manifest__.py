# -*- coding: utf-8 -*-
{
    'name': "Entradas y Salidas de caja",
    'summary': """Modulo Caja""",
    'description': """
        Modulo de Entradas y Salidas de Caja
    """,
    'author': "Moogah",
    'website': "http://www.Moogah.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'account',
        'account_payment_fix',
        'account_check',
        'account_withholding',
        'hr',
        'vitt_account_subtype',
     ],
    'data': [
        'data/sequence.xml',
        'views/cash_view.xml',
        'views/res_partner.xml',
        'wizard/change_check_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'application': True,
}