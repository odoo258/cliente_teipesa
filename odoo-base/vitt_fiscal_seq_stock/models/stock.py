# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning, ValidationError
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class stock_picking(models.Model):
    _inherit = 'stock.picking'
    fiscal_control = fields.Boolean('Fiscal Control', help='If the inventory move is Fiscal', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, copy=False)
    fiscal_secuence = fields.Many2one('ir.sequence', string='Fiscal Secuence', help='Fiscal Secuence', store=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, copy=False)
    fiscal_number = fields.Char('Fiscal Number', help='Fiscal Number', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, copy=False)

    def _get_fiscal_sequence(self):
        fiscal_sequence_domain = [
            ('sequence_id', '=', self.fiscal_secuence.id),
        ]
        fiscal_sequence = self.env['vitt_fiscal_seq.fiscal_sequence_regime'].search(fiscal_sequence_domain, limit=1)

        return fiscal_sequence

    @api.onchange('fiscal_secuence')
    def _onchange_fiscal_secuence(self):
        if self.fiscal_secuence:
            next_number = self.fiscal_secuence.number_next_actual
            self.fiscal_number = self.fiscal_secuence.get_next_char(next_number)

    @api.onchange('fiscal_control')
    def _onchange_fiscal_control(self):
        if self.fiscal_control:
            sequence_domain = [
                ('company_id', '=', self.company_id.id),
                ('code', '=', 'remission'),
                ('active', '=', True),
            ]
            next_number = self.fiscal_secuence.number_next_actual
            sequence = self.env['ir.sequence'].search(sequence_domain, limit=1)
            if sequence:
                self.fiscal_secuence = sequence.id
                self.fiscal_number = self.fiscal_secuence.get_next_char(next_number)
        else:
            self.fiscal_secuence = ''
            self.fiscal_number = ''

    @api.one
    @api.constrains('fiscal_control')
    def _check_fiscal_control(self):
        if self.fiscal_control:
            if not self.fiscal_number:
                raise ValidationError("Required Fiscal Number")

    @api.one
    @api.constrains('fiscal_number')
    def _check_fiscal_number(self):
        if self.fiscal_control and self.fiscal_number:
            fiscal_sequence = self._get_fiscal_sequence()

            # check if is already in use
            move_domain = [
                ('company_id', '=', self.company_id.id),
                ('fiscal_number', '=', self.fiscal_number),
                ('id', '!=', self.id),
            ]
            move = self.env['stock.picking'].search(move_domain, limit=1)
            if move:
                msgstr = "This Fiscal Number is already in use  %s" % move.name
                raise ValidationError(msgstr)

            # check if date and number is in range
            if self.fiscal_secuence.id:
                if fiscal_sequence:
                    code_authorization = fiscal_sequence.authorization_code_id
                    if not self.min_date:
                        dt = str(fields.date.today())
                    else:
                        dt = self.min_date

                    if (dt < code_authorization.start_date) or (dt > code_authorization.expiration_date):
                        raise ValidationError(_('The date %s is not allowed in this sequence') % (dt))

            if self.fiscal_number:
                padding = self.fiscal_secuence.padding
                the_number = self.fiscal_number[-padding:]
                number = int(the_number)
                if (number < fiscal_sequence._from) or (number > fiscal_sequence._to):
                    raise ValidationError(_('The Number %s is not allowed in this sequence') % (number))

    def _set_number_next_actual(self):
        # fiscal_sequence = self._get_fiscal_sequence()
        padding = self.fiscal_secuence.padding
        the_number = self.fiscal_number[-padding:]

        next_number = int(the_number) + 1
        if next_number > self.fiscal_secuence.number_next_actual:
            self.fiscal_secuence.write({'number_next_actual': next_number})

    @api.multi
    def do_new_transfer(self):
        res = super(stock_picking, self).do_new_transfer()
        if self.fiscal_number:
            self._set_number_next_actual()
        return res
