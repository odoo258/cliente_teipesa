# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        res.update({'customer': False})
        return res
