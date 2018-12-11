# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning, ValidationError

SUPP_INVOICE = ['in_invoice', 'in_refund']


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fiscal_number = fields.Char('Fiscal Number', help='Fiscal Number', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, copy=False)
    fiscal_control = fields.Boolean(copy=False)

    def is_supplier_inv(self):
        if self.type in SUPP_INVOICE:
            return True
        return False

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if inv.is_supplier_inv() and inv.move_id and inv.fiscal_number:
                inv.write({'internal_number': inv.fiscal_number})
                self._set_number_next_actual()

        return res

    # for purchase BEGIN
    def _get_fiscal_sequence(self):
        fiscal_sequence_domain = [
            ('sequence_id', '=', self.sequence_ids.id),
        ]
        fiscal_sequence = self.env['vitt_fiscal_seq.fiscal_sequence_regime'].search(fiscal_sequence_domain, limit=1)

        return fiscal_sequence

    def _set_number_next_actual(self):
        padding = self.sequence_ids.padding
        the_number = self.fiscal_number[-padding:]

        next_number = int(the_number) + 1
        if next_number > self.sequence_ids.number_next_actual:
            self.sequence_ids.write({'number_next_actual': next_number})

    @api.onchange('fiscal_control')
    def _onchange_fiscal_control_seq(self):
        if self.is_supplier_inv():
            self.sequence_ids = self._default_sequence(self.journal_id.id)
            if self.sequence_ids:
                self._onchange_fiscal_sequence_ids()

    @api.onchange('sequence_ids')
    def _onchange_fiscal_sequence_ids(self):
        if not self.sequence_ids and self.is_supplier_inv():
            self.fiscal_number = None
        if self.sequence_ids and self.is_supplier_inv():
            next_number = self.sequence_ids.number_next_actual
            self.fiscal_number = self.sequence_ids.get_next_char(next_number)

    @api.one
    @api.constrains('fiscal_number')
    def _check_fiscal_number(self):
        if self.is_supplier_inv() and self.fiscal_control and self.fiscal_number:
            fiscal_sequence = self._get_fiscal_sequence()

            # check if is already in use
            account_domain = [
                ('company_id', '=', self.company_id.id),
                ('fiscal_number', '=', self.fiscal_number),
                ('id', '!=', self.id),
            ]
            invoice = self.env['account.invoice'].search(account_domain, limit=1)
            if invoice:
                tstr = invoice.number or invoice.reference or invoice.state
                msgstr = "This Fiscal Number is already in use  %s" % tstr
                raise ValidationError(msgstr)

            # check if date and number is in range
            if self.sequence_ids:
                if fiscal_sequence:
                    code_authorization = fiscal_sequence.authorization_code_id
                    if not self.date_invoice:
                        dt = str(fields.date.today())
                    else:
                        dt = self.date_invoice

                    if (dt < code_authorization.start_date) or (dt > code_authorization.expiration_date):
                        raise ValidationError(_('The date %s is not allowed in this sequence') % (dt))

            if self.fiscal_number:
                padding = self.sequence_ids.padding
                the_number = self.fiscal_number[-padding:]
                number = int(the_number)
                if (number < fiscal_sequence._from) or (number > fiscal_sequence._to):
                    raise ValidationError(_('The Number %s is not allowed in this sequence') % (number))

    # for purchase END
