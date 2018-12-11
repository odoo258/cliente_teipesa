# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 BACG S.A. de C.V. (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': 'VITT - Format Print - Account Move',
    'summary': 'Setup multiple print formats to Account Moves',
    'version': '1.0',
    "author": "Business Analytics Consulting Group S.A. de C.V.",
    'website': 'http://www.bacgroup.net',
    'category': 'Accounting',
    'description': """
        Setup multiple print formats to Invoice
    """,
    'depends': ['base', 'account', 'vitt_format_print'],
    'data': [
        'data/data.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
