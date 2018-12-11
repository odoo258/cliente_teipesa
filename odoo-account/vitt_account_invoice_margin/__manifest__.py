# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "Account Invoice Margin",
    'description': """
    View Margin and Cost on invoice \n

    Configure;\n
        * User Rights --> View Cost Invoice / View Margin Invoice
    """,
    'summary': 'View Margin on invoice',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '1.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Accounting',

    'depends': ['base', 'account'],
    'data': [
        'views/account_invoice_view.xml',
        'security/groups.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
