# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Fiscal Sequences - Stock",
    'description': 'Add Stock Fiscal Sequences Feature',
    'summary': '',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '10.0.1.0',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'stock',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'vitt_fiscal_seq'],

    # always loaded
    'data': [
        'views/stock.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
