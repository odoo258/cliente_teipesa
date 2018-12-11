# -*- coding: utf-8 -*-

##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, fields, models, _


class AccountConfigSettings(models.Model):
    _inherit = 'res.company'

    legend_ids = fields.One2many(
        "account.legend",
        "company_id",
        "Legends"
    )
