# -*- coding: utf-8 -*-

##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, fields, models, _


class AccountLegend(models.Model):
    _name = "account.legend"

    _description = "Legends for invoices"

    name = fields.Char("Legend Name")
    company_id = fields.Many2one(
        "res.company",
        string="Related Company",
        ondelete="cascade"
    )
