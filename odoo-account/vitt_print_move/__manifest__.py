# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Print Account Move",
    'description': 'Print the Account move ',
    'summary': '',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '0.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Accounting',
    'depends': ['base', 'account'],
    'data': [
        'report_account_move.xml',
        'views/report_move.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
