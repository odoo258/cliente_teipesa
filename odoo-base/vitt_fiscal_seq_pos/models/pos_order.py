# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    tax_authorization_code = fields.Char('code autorization', help='tax authorization code provided by the taxable entity')
    authorization_code_id = fields.Many2one('vitt_fiscal_seq.authorization_code')
    code_type = fields.Char('Tax regime code type', help='tax regime type code')
    start_date = fields.Date('Start Date', help='start date')
    expiration_date = fields.Date('Expiration Date', help='expiration date')
    _from = fields.Integer('From', help='origin value')
    _to = fields.Integer('To', help='destination value')

    @api.model
    def sequence_number_sync(self, values):
        next = values.get('_sequence_ref_number', False)
        next = int(next) if next else False
        if values.get('session_id') and next is not False:
            session = self.env['pos.session'].sudo().browse(values['session_id'])
            if next != session.config_id.sequence_fiscal_id.number_next_actual:
                session.config_id.sequence_fiscal_id.number_next_actual = next
        if values.get('_sequence_ref_number') is not None:
            del values['_sequence_ref_number']

    @api.model
    def _order_fields(self, ui_order):
        vals = super(PosOrder, self)._order_fields(ui_order)
        vals['_sequence_ref_number'] = ui_order.get('sequence_ref_number')
        vals['pos_reference'] = ui_order.get('sequence_ref')
        vals['authorization_code_id'] = ui_order.get('authorization_code_id')
        vals['tax_authorization_code'] = ui_order.get('authorization_code')
        vals['code_type'] = ui_order.get('ac_code_type')
        vals['expiration_date'] = ui_order.get('expiration_date')
        vals['_from'] = ui_order.get('min_number')
        vals['_to'] = ui_order.get('max_number')
        return vals

    @api.model
    def create(self, values):
        if values.get('session_id'):
            self.sequence_number_sync(values)

        order = super(PosOrder, self).create(values)
        return order

    @api.constrains('pos_reference')
    def _check_sequence_ref_number(self):
        if self.pos_reference:
            domain = [
                ('pos_reference', '=', self.pos_reference),
                ('id', '!=', self.id)
            ]
            pos_order_obj = self.env['pos.order'].search(domain, limit=1)
            if pos_order_obj:
                tstr = ("Already exist a ticket with this number '%s'") % (self.pos_reference)
                _logger.warning(tstr)
                raise ValidationError(_(tstr))


class PosConfig(models.Model):
    _inherit = "pos.config"

    sequence_fiscal_id = fields.Many2one(
        'ir.sequence', string='Fiscal Order IDs Sequence',
        help="This sequence must be assigned by the user for Odoo to customize the "
        "order numbers of their orders with fiscal sequence.",
        copy=False,
        domain="[('is_fiscal_sequence', '=',True), ('active', '=', True), '|', ('code', '=', 'out_invoice'), ('code','=', 'in_refund'), ('journal_id', '=', journal_id)]"
    )
    authorization_code_id = fields.Many2one('vitt_fiscal_seq.authorization_code', store=True, readonly=True, compute='_compute_authorization_code_id')

    @api.one
    @api.depends('sequence_fiscal_id')
    def _compute_authorization_code_id(self):
        if self.sequence_fiscal_id:
            code_authorization = False
            for fiscal_seq in self.sequence_fiscal_id.fiscal_sequence_regime_ids:
                if fiscal_seq.authorization_code_id.active:
                    code_authorization = fiscal_seq.authorization_code_id
                    break
            if code_authorization:
                self.authorization_code_id = code_authorization.id
        else:
            return

    @api.one
    @api.constrains('sequence_fiscal_id')
    def _check_sequence_fiscal_id(self):
        if self.sequence_fiscal_id:
            if not self.sequence_fiscal_id.is_fiscal_sequence:
                raise Warning(_('Error! Select a Fiscal Sequence'))

        duplicated = self.search_count([('sequence_fiscal_id', '=', self.sequence_fiscal_id.id)])

        if self.sequence_fiscal_id and duplicated > 1:
            raise ValidationError(_("You can not have two or more active POS with the same Fiscal Sequence"))
