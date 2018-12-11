# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class AccountAssetCategory(models.Model):
    _inherit = 'account.asset.category'

    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')


class AccountAssetDepreciationLine(models.Model):
    _inherit = 'account.asset.depreciation.line'

    @api.multi
    def create_move(self, post_move=True):
        res = super(AccountAssetDepreciationLine, self).create_move()
        account_move = self.env['account.move'].browse(res)
        for dep in self:
            category_id = dep.asset_id.category_id
            analytic_tags = self.env['account.analytic.tag']._set_tags(tags=dep.asset_id.analytic_tag_ids, new_tags=category_id.analytic_tag_ids + category_id.account_analytic_id.tag_ids)
            for move in account_move:
                for move_line in move.line_ids:
                    move_line.write({'analytic_tag_ids': [(6, 0, analytic_tags.ids)]})
        return res

    @api.multi
    def create_grouped_move(self, post_move=True):
        res = super(AccountAssetDepreciationLine, self).create_grouped_move()
        analytic_tag_obj = self.env['account.analytic.tag']
        account_move = self.env['account.move'].browse(res)
        depreciation_tags_ids = []
        for dep in self:
            category_id = dep.asset_id.category_id
            depreciation_tags_ids += category_id.analytic_tag_ids.ids + category_id.account_analytic_id.tag_ids.ids + dep.asset_id.analytic_tag_ids.ids

        depreciation_tags_ids = list(set(depreciation_tags_ids))
        depreciation_tags = analytic_tag_obj.browse(depreciation_tags_ids)
        analytic_tags = analytic_tag_obj._set_tags(tags=depreciation_tags, new_tags=depreciation_tags)
        for move in account_move:
            for move_line in move.line_ids:
                move_line.write({'analytic_tag_ids': [(6, 0, analytic_tags.ids)]})

        return res
