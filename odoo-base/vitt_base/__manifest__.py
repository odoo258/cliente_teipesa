# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Base Module",
    'description': 'Base Tools for Generic Latin American Localization',
    'summary': '',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '1.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Hidden',

    'sequence': 1050,
    'depends': ['base', 'sales_team', 'account', 'account_accountant', 'stock', 'purchase', 'sale', 'base_vat'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/partners_views.xml',
        'views/sale_order_view.xml',
        'views/settings_view.xml',
        'views/vitt_base_settings_view.xml',
    ],
    'demo': [
    ],
    'installable': False,
    'application': False,
    'auto_install': False,
}
