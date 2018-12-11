# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2017 OpenERP SA (<http://www.serpentcs.com>)
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
    'name': 'Pos Fiscal Printer',
    'version': '10.0.0.1',
    'category': 'Point Of Sale',
    'sequence': 6,
    'summary': 'Interface to Point of Sale',
    'description':'/static/description/index.html',
    'author': 'Serpent Consulting Services Pvt. Ltd',
    'website': 'serpentcs.com',
    'installable': True,
    'application': True,
    'data': [
           'view/template.xml',
           'view/pos_orders.xml'
           ],
    'depends': ['point_of_sale','pos_backend_receipt','hw_proxy'],
    'auto_install': False,
}
