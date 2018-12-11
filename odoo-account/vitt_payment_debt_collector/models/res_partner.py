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


class Partner(models.Model):
    _inherit = 'res.partner'

    debt_collector = fields.Many2one('res.users', string='Debt Collector', help='Debt Collector', ondelete='restrict')

