# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    'name': "VITT Payment Debt Collector",
    'summary': 'Apply Payment Debt Collector',
    'description': '''
    This app assigns a debt collector for each of the clients. \n
    - Sales>>Sales>>Customer

    Configure;\n
        * Payment
        
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
        'views/res_partner_view.xml',
		'views/account_payment_view.xml'

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
