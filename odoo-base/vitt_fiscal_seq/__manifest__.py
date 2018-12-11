# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  BACG S.A. de C.V.  (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    'name': "VITT Fiscal Sequences - Base",
    'summary': """
        VITT Fiscal Sequences - Base
        """,
    'description': """
        VITT Fiscal Sequences - Base
    """,
    'author': 'Business Analytics Consulting Group S.A. de C.V.',
    'website': 'www.bacgroup.net',
    'version': '1.1',
    'license': 'Other proprietary',
    'maintainer': '',
    'contributors': '',
    'category': 'Extra Tools',
    'depends': ['base', 'account', 'vitt_jrseq'],
    'data': [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "wizard/journal_settings_view.xml",
        "views/config_journal_view.xml",
        "views/config_authorization_code_view.xml",
        "views/ir_sequence_view.xml",
        "views/account_invoice_view.xml",
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
