# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields


class sale_order(models.Model):
    _inherit = 'sale.order'

    order_type = fields.Many2one('vitt_base.order_type', string='Order Type', help='Order Type', ondelete='restrict')
    sales_order_type = fields.Boolean(related='company_id.sales_order_type', default='company_id.sales_order_type', store=False)


class order_type(models.Model):
    _name = "vitt_base.order_type"
    name = fields.Char('Name', help='Order Name', required=True)
    description = fields.Char('Description', help='Order description', required=True)

    _sql_constraints = [
        ('value_order_uniq', 'unique (name)', 'Only a unique Order Type is permitted!')
    ]
