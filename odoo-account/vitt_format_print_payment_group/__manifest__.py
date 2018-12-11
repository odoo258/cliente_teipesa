# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 BACG S.A. de C.V. (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': 'VITT - Format Print - Payment group',
    'summary': 'Setup multiple print formats to Payment Groups',
    'version': '1.0',
    "author": "Business Analytics Consulting Group S.A. de C.V.",
    'website': 'http://www.bacgroup.net',
    'category': 'Sales',
    'description': """
        Setup multiple print formats to Payment Groups
    """,
    'depends': ['base', 'account_payment_group', 'vitt_format_print'],
    'data': [
        'views/sale_paymgroup_view.xml',
        'data/data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
