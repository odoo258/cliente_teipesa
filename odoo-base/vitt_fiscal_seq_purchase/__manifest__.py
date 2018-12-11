# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': "VITT Fiscal Sequences - Purchase",
    'summary': """
        VITT Fiscal Sequences - Purchase
        """,
    'description': """
        VITT Fiscal Sequences - Purchase
    """,
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '1.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Extra Tools',
    'depends': ['base', 'account', 'vitt_fiscal_seq'],
    'data': [
        "views/account_invoice_view.xml",
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
