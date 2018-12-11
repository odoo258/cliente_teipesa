# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api, _


class res_partner(models.Model):
    _inherit = 'res.partner'

    birthdate = fields.Date('Birthdate', help='Birthdate')
    credit_limit = fields.Monetary('Credit Limit', help='Customer Credit Limit')
    days_credit_limit = fields.Integer('Days Credit Limit', help='Customer Days Credit Limit')
    purchase_limit = fields.Monetary('Purchase Limit', help='Customer Purchase Limit')
    days_purchase_limit = fields.Monetary('Days Purchase Limit', help='Customer Days Purchase Limit')
    document_type = fields.Selection([('id', 'ID'), ('passport', 'Passport'), ('driving_license', 'Driving license'), ], string='Customer Document Type', help='Customer Document Type')
    nationality = fields.Many2one('res.country', string='Nationality', help='Nationality', ondelete='restrict')
    place_birth = fields.Many2one('res.country', string='Place of Birth', help='Place of Birth', ondelete='restrict')
    profession = fields.Many2one('vitt_base.profession', string='Profession', help='Profession', ondelete='restrict')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ], string='Gender', help='Gender')
    civil_status = fields.Selection([('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('other', 'Other'), ], string='Civil Status', help='Civil Status')
    document_number = fields.Char('Document Number', help='Document Number')
    other_company_reg = fields.Char('Other Company Registry', help='Other Company Registry for some countries')
    partner_extrainfo = fields.Boolean(related='company_id.partner_extrainfo', default='company_id.partner_extrainfo', store=False)
    partner_unique_vat = fields.Boolean(related='company_id.partner_unique_vat', default='company_id.partner_unique_vat', store=False)

    @api.one
    @api.constrains('vat')
    def _check_unique_vat(self):
        if self.partner_unique_vat:
            if self.vat:
                partner_ids = self.search(
                    [('vat', '=', self.vat),
                     ('id', '!=', self.id)])
                for partner in partner_ids:
                    if not((partner.child_ids and self.id in partner.child_ids.ids)
                           or (partner.parent_id and
                               self.parent_id == partner.parent_id)):
                        raise Warning(_(
                            'Error! VAT Number already exists'))


class profession(models.Model):
    _name = "vitt_base.profession"
    name = fields.Char('Name', help='Profession Name', required=True)
    description = fields.Char('Description', help='Profession description', required=True)

    _sql_constraints = [
        ('value_profession_uniq', 'unique (name)', 'Only a unique Profession is permitted!')
    ]
