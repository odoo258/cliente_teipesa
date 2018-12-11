# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning

# mapping invoice type to journal type
TYPE2JOURNAL = {
    'out_invoice': 'sale',
    'in_invoice': 'purchase',
    'out_refund': 'sale',
    'in_refund': 'purchase',
}

CUST_INVOICE = ['out_invoice', 'out_refund']


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def is_customer_inv(self):
        if self.type in CUST_INVOICE:
            return True
        return False

    @api.multi
    @api.depends("company_id")
    def _default_fiscal_validated(self, company_id):
        if company_id:
            fiscal_sequence_ids = self.env["vitt_fiscal_seq.authorization_code"].search([('company_id', '=', company_id), ('active', '=', True)])
            if fiscal_sequence_ids:
                return True
            else:
                return False

    @api.multi
    @api.depends("journal_id")
    def _default_sequence(self, journal_id):
        flag = 0
        domain = [
            ('is_fiscal_sequence', '=', True),
            ('active', '=', True),
            ('journal_id', '=', journal_id),
            '|',
            ('code', '=', self.type),
            ('code', '=', 'in_refund'),
            '|',
            ('user_ids', 'in', self.user_id.id),
            ('user_ids', 'in', False),
        ]
        sequence = self.env['ir.sequence'].search(domain)
        for count in sequence:
            flag += 1
        if flag == 1:
            return self.env['ir.sequence'].search(domain)

    fiscal_control = fields.Boolean('Fiscal Control', help='If is a Fiscal Document')
    # Unique number of the invoice, computed automatically when the invoice is created
    internal_number = fields.Char(string='Invoice Number', readonly=True, default=False, help="Unique number of the invoice, computed automatically when the invoice is created.", copy=False)
    sequence_ids = fields.Many2one("ir.sequence", "Fiscal Sequence", states={'draft': [('readonly', False)]},
                                   domain="[('is_fiscal_sequence', '=',True),('active', '=', True), '|',('code','=', type),('code','=', 'in_refund'),('journal_id', '=', journal_id), '|', ('user_ids','in',False),('user_ids','in', user_id)]")

    @api.model
    def create(self, vals):
        if not vals.get("sequence_ids") and (vals.get('type') in CUST_INVOICE):
            vals["fiscal_control"] = 0
            vals["sequence_ids"] = 0
            if vals.get("company_id"):
                company_id = vals.get("company_id")
                vals["fiscal_control"] = self._default_fiscal_validated(vals.get("company_id"))
            else:
                company_id = self.env["res.users"].browse(vals.get("user_id")).company_id.id
                vals["fiscal_control"] = self._default_fiscal_validated(company_id)

            user_default_journal = self.env['ir.values'].get_default('account.invoice', 'journal_id', for_all_users=False, company_id=company_id)
            seq = None

            journal_id = vals.get("journal_id")
            if user_default_journal:
                journal_id = user_default_journal
                vals['journal_id'] = user_default_journal

            if vals.get("journal_id") and not vals["fiscal_control"]:
                company_id = self.env["account.journal"].browse(vals.get("journal_id")).company_id.id
                vals["fiscal_control"] = self._default_fiscal_validated(company_id)

            if vals["fiscal_control"] and vals.get("journal_id"):
                user_default_sequence = self.env['ir.values'].get_default('account.invoice', 'sequence_ids', for_all_users=False, company_id=company_id)
                if not user_default_sequence:
                    flag = 0
                    domain = [
                        ('is_fiscal_sequence', '=', True),
                        ('active', '=', True),
                        ('journal_id', '=', vals.get("journal_id")),
                        ('code', '=', vals.get("type"))]
                    sequence = self.env["ir.sequence"].search(domain)
                    for count in sequence:
                        flag += 1
                    if flag == 1:
                        seq = self.env['ir.sequence'].search(domain).id
                else:
                    sequence = self.env["ir.sequence"].browse(user_default_sequence)
                    journal_id = sequence.journal_id.id

                vals["sequence_ids"] = user_default_sequence or seq
                vals["journal_id"] = journal_id

        invoice = super(AccountInvoice, self).create(vals)
        return invoice

    @api.onchange('journal_id')
    def _onchange_journal_inh(self):
        self.fiscal_control = self._default_fiscal_validated(self.company_id.id)
        self.sequence_ids = self._default_sequence(self.journal_id.id)

    @api.multi
    def action_date_assign(self):
        res = super(AccountInvoice, self).action_date_assign()
        if self.sequence_ids:
            if self.date_invoice > self.sequence_ids.expiration_date:
                raise Warning(_('The Expiration Date for this fiscal sequence is %s ') % (self.sequence_ids.expiration_date))
            if self.sequence_ids.vitt_number_next_actual > self.sequence_ids.max_value:
                raise Warning(_('The range of sequence numbers is finished'))
        return res

    @api.onchange("company_id")
    def onchange_company_id(self):
        flag = 0
        fiscal_sequence_ids = self.env["vitt_fiscal_seq.authorization_code"].search([('company_id', '=', self.company_id.id), ('active', '=', True)])
        company = self.env["res.company"].search([('id', '>', 0)])
        for count in company:
            flag += 1
        if fiscal_sequence_ids:
            self.fiscal_control = True
        else:
            self.fiscal_control = False
        # TODO: Revisar este tema de onchange por lo momentos se dejara por defecto como viene
        # if flag > 1:
        #    domain = [
        #        ('type', '=', self.type),
        #        ('company_id', '=', self.company_id.id),
        #    ]
        #    self.journal_id = self.env['account.journal'].search(domain).id

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if inv.move_id and self.is_customer_inv():
                if not inv.internal_number:
                    if self.fiscal_control and self.sequence_ids:
                        new_name = self.sequence_ids.with_context(ir_sequence_date=inv.move_id.date).next_by_id()
                        inv.move_id.write({'name': new_name})
                        inv.write({'internal_number': new_name})
                else:
                    inv.move_id.write({'name': inv.internal_number})
        return res
