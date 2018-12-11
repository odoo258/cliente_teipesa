# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import datetime
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import sys
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _discount_move_lines(self, i_line):
        res = []
        fpos = i_line.invoice_id.fiscal_position_id
        accounts = i_line.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fpos)
        cost_tot = discount_tot = disc_amount = 0.0

        tax_ids = []
        for tax in i_line.invoice_line_tax_ids:
            tax_ids.append((4, tax.id, None))
            for child in tax.children_tax_ids:
                if child.type_tax_use != 'none':
                    tax_ids.append((4, child.id, None))
        analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in i_line.analytic_tag_ids]

        move_line_vals = {
            'invl_id': i_line.id,
            'type': 'src',
            'name': i_line.name[:64],
            'product_id': i_line.product_id.id,
            'uom_id': i_line.uom_id.id,
            'account_analytic_id': i_line.account_analytic_id.id,
            'tax_ids': tax_ids,
            'invoice_id': self.id,
            'analytic_tag_ids': analytic_tag_ids
        }

        if i_line['account_analytic_id']:
            move_line_vals['analytic_line_ids'] = [(0, 0, i_line._get_analytic_line())]

        if i_line.discount:
            # Debit Line
            move_line_disc_tot = {}
            move_line_disc_tot['account_id'] = i_line.discount_account_id.id
            move_line_disc_tot['price_unit'] = self.currency_id.compute(-i_line.discount_value, self.env.user.company_id.currency_id)
            move_line_disc_tot['quantity'] = i_line.quantity
            move_line_disc_tot['price'] = self.currency_id.compute(-i_line.discount_value, self.env.user.company_id.currency_id)
            move_line_disc_tot.update(move_line_vals)
            move_line_disc_tot['name'] = _('Discount - %s' % (i_line.name[:64]))

            res.append(move_line_disc_tot)

            # Credit Line
            move_line_cre_tot = {}
            move_line_cre_tot['account_id'] = i_line.account_id.id
            move_line_cre_tot['price_unit'] = self.currency_id.compute(i_line.discount_value, self.env.user.company_id.currency_id)
            move_line_cre_tot['quantity'] = i_line.quantity
            move_line_cre_tot['price'] = self.currency_id.compute(i_line.discount_value, self.env.user.company_id.currency_id)
            move_line_cre_tot.update(move_line_vals)
            move_line_cre_tot['name'] = _('Discount - %s' % (i_line.name[:64]))

            res.append(move_line_cre_tot)

        return res


    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        if self.type in ('out_invoice', 'out_refund'):
            for i_line in self.invoice_line_ids:
                res.extend(self._discount_move_lines(i_line))
        return res



class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    discount_account_id = fields.Many2one('account.account', related='company_id.property_account_discount_id' ,readonly=True, help="Discount account used for this invoice")
    discount_value = fields.Float('Discount Value', compute='_get_discount', help="Discount Value")

    @api.multi
    @api.depends('discount')
    def _get_discount(self):
        for invoice in self:
            if invoice.discount > 0:
               price_total = invoice.price_unit * invoice.quantity
               discount_total = price_total - invoice.price_subtotal
               invoice.discount_value = discount_total