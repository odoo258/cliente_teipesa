# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': "VITT Numbers to Words in pos",
    'description': """
    Add Feature to Convert Numbers to Words \n
    Configure; \n
    - Accounting>>Settings>>Values in words
    - Accounting>>Settings>>Settings>>Company Settings; Set Default Language to convert Numbers to words
    """,
    'summary': 'Convert Numbers to Words in Point Of Sale',
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '0.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Extra Tools',
    'depends': ['web', 'point_of_sale', 'vitt_val2words'],
    'data': [
        'views/view.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'js': [
        'static/src/js/val2text.js'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
