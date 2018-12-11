# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    transport_id = fields.Many2one('res.partner', string='Transport')
