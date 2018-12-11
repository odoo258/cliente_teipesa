# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 BACG S.A. de C.V. (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': 'VITT - Format Print - Payment',
    'summary': 'Setup multiple print formats to Payments',
    'version': '1.0',
    "author": "Business Analytics Consulting Group S.A. de C.V.",
    'website': 'http://www.bacgroup.net',
    'category': 'Accounting',
    'description': """
        Setup multiple print formats to Payments
    """,
    'depends': ['base', 'account', 'vitt_format_print'],
    'data': [
        'data/data.xml',
        'views/account_payment_view.xml',
        # 'views/format_print_template.xml',
    ],
    'installable': True,
    'auto_install': False,
}
