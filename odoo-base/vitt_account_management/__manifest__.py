# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Account Management",
    'summary': 'Basic account setup',
    'description': '''
    This app allows to setup main accounts for Debtors, Creditors, Income, Expenses and Exchange Rates. \n
    These accounts will be used by default without the need to install a Chart of Accounts Template \n
    - Accounting>>Settings>>Settings>>VITT Account Management, Settings \n

    Configure;\n
        * Receivable Account
        * Payable Account
        * Income Account on Product Category
        * Expense Account on Product Category
        * Income Account on Product
        * Expense Account on Product
        * Stock Input Account on Product Category
        * Stock Output Account on Product Category
        * Stock Valuation Account on Product Category
        * Inter-Banks Transfer Account
        * Gain Exchange Rate Account
        * Loss Exchange Rate Account
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
        "views/account_management_view.xml",

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
