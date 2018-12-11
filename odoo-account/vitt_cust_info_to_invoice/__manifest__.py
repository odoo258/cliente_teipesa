# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Customer Info to Invoice",
    'summary': 'Add Info From Customer to the Invoice',
    'description': '''
    Add Info From Customer to the Invoice\n
    - Salesperson
    ''',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '1.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Extra Tools',

    'sequence': 1050,
    'depends': ['base', 'account'],
    'data': [
        # "views/account_invoice_view.xml",

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
