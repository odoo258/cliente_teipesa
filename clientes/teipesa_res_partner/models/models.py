# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
     _inherit = 'res.partner'

     entityf = fields.Boolean(string="Is an Entity",translate=True)
     entity = fields.Many2one('res.partner',string="Entity",domain="[('entityf', '=', True),('id', '!=', id)]",translate=True)
     passwd = fields.Char(size=64,string="Password",translate=True)


class AccountInvoiceLine(models.Model):
     _inherit = 'account.invoice.line'

     cons_value = fields.Float(string="Cons. %",translate=True,readonly=True)

class SaleOrder(models.Model):
     _inherit = 'sale.order'

     external_reference = fields.Char(string="External Reference",translate=True,readonly=True)
