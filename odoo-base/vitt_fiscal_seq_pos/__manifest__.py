# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 BACG S.A. de C.V. (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': "VITT Fiscal Sequences - POS",
    'version': '0.1',
    'category': 'Point Of Sale',
    "author": "Business Analytics Consulting Group S.A. de C.V.",
    'summary': 'Sequential Order numbers for Point of sale',
    'depends': [
        "point_of_sale",
        "vitt_fiscal_seq",
    ],
    'data': [
        'views/pos_template.xml',
        'views/pos_order_view.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
