# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 BACG S.A. de C.V. (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################

{
    "name": 'Account Report Invoice Copies',
    "version": '0.1',
    "description": """
        Use;
        
        - Accounting>>Sales>>Invoices Customer, menu "Print", Invoices and Copies

        Configure;\n

        - Accounting>>Configuration>>Configure your company data. Field 'Legends': Add as many copies as you want
        - User Access; Allow "Invoice Reprint"
    """,
    "author": "Business Analytics Consulting Group S.A. de C.V.",
    "website": 'http://www.bacgroup.net',
    "depends": [
        'account'
    ],
    "data": [
        "security/security.xml",
        "views/config_view.xml",
        "views/vitt_external_layout.xml",
        "views/vitt_footer.xml",
        "views/vitt_report_invoice.xml",
        "reports/account_report.xml",
    ],
    "demo": [],
    "installable": True,
    "active": False,
    "category": 'Reporting',
    "test": [],
}
