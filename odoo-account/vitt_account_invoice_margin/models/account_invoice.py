# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api
from .. import utils


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    margin = fields.Monetary('Invoice Total Margin', help='Invoice Total Margin', readonly=True)

    @api.multi
    def _compute_margin(self):
        self.margin = 0
        if self.invoice_line_ids:
            for line in self.invoice_line_ids:
                self.margin = self.margin + line.margin

    @api.multi
    def recalc_line_cost(self):
        if self.invoice_line_ids:
            for line in self.invoice_line_ids:
                line._product_margin()
                line._compute_cost(line.invoice_id, line.product_id)

    @api.onchange('invoice_line_ids')
    def _on_change_line_ids_margin(self):
        self._compute_margin()

    @api.multi
    def action_date_assign(self):
        self.recalc_line_cost()
        self._compute_margin()
        return super(account_invoice, self).action_date_assign()


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    cost = fields.Monetary('Product Cost', help='Product Cost', store=True, readonly=True, compute="_product_margin")
    cost_total = fields.Monetary('Product Cost Total', help='Product Cost Total', store=True, readonly=True, compute="_product_margin")
    margin = fields.Monetary('Product Margin', help='Product Margin', store=True, readonly=True, compute="_product_margin")

    def _compute_cost(self, invoice_id, product_id):
        frm_cur = self.env.user.company_id.currency_id
        to_cur = invoice_id.currency_id
        cost_price = product_id.standard_price
        ctx = self.env.context.copy()
        ctx['date'] = invoice_id.date_invoice
        costp = frm_cur.with_context(ctx).compute(cost_price, to_cur, round=False)
        return costp

    @api.one
    @api.depends('price_unit', 'quantity')
    def _product_margin(self):
        if not self.product_id:
            return
        self.cost = self._compute_cost(self.invoice_id, self.product_id)
        self.cost_total = self.quantity * self.cost
        self.margin = self.price_subtotal - self.cost_total
