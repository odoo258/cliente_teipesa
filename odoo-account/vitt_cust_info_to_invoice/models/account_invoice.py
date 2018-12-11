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

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.type in ['out_invoice', 'out_refund']:
            if self.partner_id.property_product_pricelist:
                self.currency_id = self.partner_id.property_product_pricelist.currency_id.id
            if self.partner_id.user_id:
                self.user_id = self.partner_id.user_id.id
            else:
                self.user_id = self.env.user.id

        return res
