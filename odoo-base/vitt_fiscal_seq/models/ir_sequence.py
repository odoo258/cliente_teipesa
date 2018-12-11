# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api


class Sequence(models.Model):
    _inherit = "ir.sequence"

    fiscal_sequence_regime_ids = fields.One2many("vitt_fiscal_seq.fiscal_sequence_regime", "sequence_id")
    expiration_date = fields.Date('Expiration Date')
    vitt_min_value = fields.Char('Minimal number', readonly=True)
    vitt_max_value = fields.Char('Max number', readonly=True)
    percentage_alert = fields.Float('percentage alert', default=80)
    percentage = fields.Float('percentage', compute='compute_percentage')
    vitt_prefix = fields.Char('Prefix', related='prefix')
    vitt_padding = fields.Integer('Number padding', related='padding')
    vitt_number_next_actual = fields.Integer('Next Number', related='number_next_actual')
    is_fiscal_sequence = fields.Boolean("Fiscal sequence")
    user_ids = fields.Many2many("res.users", string="Users")

    @api.depends('min_value')
    def display_minimal_value(self):
        if self.vitt_prefix:
            start_number_filled = str(self.min_value)
            for filled in range(len(str(self.min_value)), self.vitt_padding):
                start_number_filled = '0' + start_number_filled
            self.vitt_min_value = self.vitt_prefix + str(start_number_filled)

    @api.depends('max_value')
    def display_max_value(self):
        if self.vitt_prefix:
            final_number = self.max_value
            final_number_filled = str(self.max_value)
            for filled in range(len(str(final_number)), self.vitt_padding):
                final_number_filled = '0' + final_number_filled
            self.vitt_max_value = self.vitt_prefix + str(final_number_filled)

    @api.one
    @api.depends('number_next_actual')
    def compute_percentage(self):
        numerator = float(self.number_next_actual - self.min_value)
        total_numbers = float(self.max_value - self.min_value)
        if total_numbers > 0:
            self.percentage = (numerator / total_numbers) * 100
        else:
            self.percentage = 0
