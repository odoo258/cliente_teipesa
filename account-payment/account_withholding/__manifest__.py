# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'author': 'Moogah,ADHOC SA',
    'website': 'www.moogah.com',
    'license': 'AGPL-3',
    'category': 'Accounting & Finance',
    'data': [
        'views/account_view.xml',
        'views/account_payment_view.xml',
        'views/account_tax_view.xml',
        'data/account_payment_method_data.xml',
        'views/account_invoice.xml',
        'views/purchase_order_view.xml',
    ],
    'depends': [
        'account',
        'purchase',
        'account_payment_group',
    ],
    'installable': True,
    'name': 'Withholdings on Payments',
    'test': [],
    'version': '10.0.1.0.1',
}
