# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError, Warning, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    unbalanced_flag = fields.Boolean('Unbalanced Flag', compute='_compute_totals',)
    t_debit = fields.Float('Debit Total', compute='_compute_totals',)
    t_credit = fields.Float('Credit Total', compute='_compute_totals',)
    unbalanced_diff = fields.Float('Unbalanced Diff', compute='_compute_totals',)

    def _onchange_do_balance_rows(self):
        self.t_debit = abs(sum(self.line_ids.mapped('debit')))
        self.t_credit = abs(sum(self.line_ids.mapped('credit')))
        self.unbalanced_diff = -sum(self.line_ids.mapped('balance'))
        if self.unbalanced_diff:
            self.unbalanced_flag = True

    @api.multi
    @api.depends('line_ids.debit', 'line_ids.credit')
    def _compute_totals(self):
        for rec in self:
            rec._onchange_do_balance_rows()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    rate = fields.Float('Rate', compute='_compute_rate', digits=(12, 6))
    do_balance = fields.Boolean(string='Do balance', default=None)

    @api.multi
    @api.depends('currency_id')
    def _compute_rate(self):
        for rec in self:
            if rec.currency_id:
                rec.rate = rec.currency_id.with_context(dict(self._context or {}, date=rec.move_id.date)).rate

    @api.onchange('amount_currency', 'currency_id')
    def _onchange_amount_currency(self):
        if self.amount_currency and self.rate:
            if self.amount_currency > 0.0:
                self.debit = self.amount_currency / self.rate
                self.credit = 0.0
            else:
                self.debit = 0.0
                self.credit = abs(self.amount_currency) / self.rate

    # @api.onchange('account_id')
    # def _onchange_account_id_ag(self):
    #     if self.account_id:
    #         self.name = self.account_id.name

    @api.onchange('do_balance')
    def _onchange_do_balance(self):
        if self.move_id.unbalanced_diff == 0.0:
            self.do_balance = None
            return

        if self.debit or self.credit:
            self.do_balance = None
            raise ValidationError(_('Balance Move only in The Last Line'))

        if self.move_id.unbalanced_diff > 0:
            self.debit = abs(self.move_id.unbalanced_diff)
            self.credit = 0.0
        else:
            self.debit = 0.0
            self.credit = abs(self.move_id.unbalanced_diff)

        self.do_balance = None
