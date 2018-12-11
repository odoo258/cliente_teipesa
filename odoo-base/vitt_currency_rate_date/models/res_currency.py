# -*- coding: utf-8 -*-

##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api


class Currency(models.Model):
    _inherit = "res.currency.rate"

    name = fields.Date(string='Date', required=True, index=True,
                       default=lambda self: fields.Date.today())

    _sql_constraints = [
        ('unique_name_per_day', 'unique (name,currency_id,company_id)', 'Only one currency rate per day allowed!'),
    ]
