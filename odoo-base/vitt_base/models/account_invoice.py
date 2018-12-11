# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api
from .. import utils


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    partner_name_audit = fields.Char('Customer Name Audit', help='Customer Name Audit', store=True)
    number = fields.Char(readonly=False)
    rate = fields.Float('Rate', help='Rate', digits=(12, 6))
    invoice_product_cost = fields.Boolean(related='company_id.invoice_product_cost', default='company_id.invoice_product_cost', store=False)

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.partner_name_audit = self.partner_id.name

    @api.onchange('currency_id')
    def _onchange_currency(self):
        self.rate = self._get_rate()