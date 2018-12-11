# -*- coding: utf-8 -*-

##############################################################################
#
#    Copyright (C) 2017 BACG S.A. de C.V. (http://www.bacgroup.net)
#    All Rights Reserved.
#
##############################################################################
{
    "name": "Vitt Base VAT",
    "summary": "allow specify the vat nr in account",
    "version": "1.1",
    "category": "Accounting",
    "website": "http://www.bacgroup.net",
    "author": "Business Analytics Consulting Group S.A. de C.V.",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "account",
    ],
    "data": [
        "views/account_invoice_view.xml"
    ],
    "qweb": [
    ]
}