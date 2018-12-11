# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    @api.multi
    def open_vitt_settings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'VITT Setting',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'vitt_base.config_settings',
            'target': 'new',
        }


class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    @api.multi
    def open_vitt_settings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'VITT Setting',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'vitt_base.config_settings',
            'target': 'new',
        }


class ResCompany(models.Model):
    _inherit = 'res.company'

    partner_extrainfo = fields.Boolean('Partner Extra Info', help='partner extra info')
    partner_unique_vat = fields.Boolean('Unique Partner by VAT', help='Unique Partner by VAT')
    invoice_product_cost = fields.Boolean('Invoice Product Cost', help='invoice product Cost')
    invoice_product_margin = fields.Boolean('Invoice Product margin', help='invoice product margin')
    sales_order_type = fields.Boolean('Sales Order Type', help='sales order type')
    invoice_manual_seq = fields.Boolean('Invoice Manual Secuence', help='invoice manual secuence')


class config_settings(models.TransientModel):
    _name = "vitt_base.config_settings"
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', help='code of company', required=True, select=1, default=lambda self: self.env.user.company_id.id, readonly=True, oldname='company')
    partner_extrainfo = fields.Boolean(related='company_id.partner_extrainfo')
    partner_unique_vat = fields.Boolean(related='company_id.partner_unique_vat')
    invoice_product_cost = fields.Boolean(related='company_id.invoice_product_cost')
    invoice_product_margin = fields.Boolean(related='company_id.invoice_product_margin')
    sales_order_type = fields.Boolean(related='company_id.sales_order_type')
    invoice_manual_seq = fields.Boolean(related='company_id.invoice_manual_seq')
