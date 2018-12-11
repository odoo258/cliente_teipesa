# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 BACG S.A. de C.V. (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': 'VITT - Format Print - Base',
    'summary': 'Base Module to Setup Multiple Formats Print',
    'version': '1.0',
    "author": "Business Analytics Consulting Group S.A. de C.V.",
    'website': 'http://www.bacgroup.net',
    'category': 'Hide',
    'description': """
        This a Base Module to Setup multiple print formats for any models
    """,
    'depends': ['base', 'vitt_val2words'],
    'data': [
        "data/data.xml",
        "security/groups.xml",
        "security/ir.model.access.csv",
        'wizard/wizard_format_print.xml',
        'views/format_print_view.xml',
        'views/format_print_template.xml',
        'format_print_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}
