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


class AccountPayment(models.Model):
    _inherit = 'account.payment'
	
    debt_collector = fields.Many2one('res.users', string='Debt Collector')
	
    @api.onchange('partner_id')
    def partner_change(self):
        self.debt_collector = self.partner_id.debt_collector