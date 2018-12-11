# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api


class SequenceJournal(models.TransientModel):
    _inherit = "vitt_fiscal_seq.journal_settings"

    doc_type = fields.Selection(selection_add=[('remission', 'Remission')])
