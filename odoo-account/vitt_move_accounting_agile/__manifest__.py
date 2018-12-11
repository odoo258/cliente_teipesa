# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Move Accounting Agile",
    'description': 'Improvements to register Account Moves',
    'summary': '',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '1.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Accounting',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
