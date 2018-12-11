# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


# class AccountConfigSettings(models.TransientModel):
#     _inherit = 'account.config.settings'

#     @api.multi
#     def open_account_management(self):
#         self.ensure_one()
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'VITT Account Management',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'vitt_account_management.config_settings',
#             'target': 'new',
#         }

class ResCompany(models.Model):
    _inherit = 'res.company'

    property_account_discount_id = fields.Many2one('account.account', string="Discount Account", help="This account will be used default")

class account_management(models.TransientModel):
    _inherit = 'vitt_account_management.config_settings'
    _inherit = 'res.config.settings'
    
    company_id = fields.Many2one('res.company', string='Company', help='Code of Company', required=True, select=1, default=lambda self: self.env.user.company_id.id, readonly=True, oldname='company')
    property_account_discount_id = fields.Many2one('account.account', related='company_id.property_account_discount_id')