# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Accounting Discount",
    'summary': 'Apply Invoice Discount',
    'description': '''
    This app allows to setup main accounts for Discounts. \n
    These accounts will be used by default without the need to install a Chart of Accounts Template \n
    - Accounting>>Settings>>Settings>>VITT Account Management, Settings \n

    Configure;\n
        * Discount Account
        
    ''',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '1.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Extra Tools',

    'sequence': 1050,
    'depends': ['base', 'account', 'vitt_account_management'],
    'data': [
        "views/account_management_view.xml",

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
