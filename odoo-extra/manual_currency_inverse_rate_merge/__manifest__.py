# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    "name" : "Manual Currency Rate And Inverse Rate Exchange In Invoice",
    "version" : "10.0.0.1",
    "depends" : ['base','account_accountant','account'],
    "author": "BrowseInfo",
    "summary": "",
    "description": """

    """,
    'category': 'Account',
    "website" : "www.browseinfo.in",
    "data" :[
             "views/currency_view.xml",
             "views/customer_invoice.xml",
             "views/account_payment_view.xml",
    ],
    'qweb':[
    ],
    "auto_install": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
