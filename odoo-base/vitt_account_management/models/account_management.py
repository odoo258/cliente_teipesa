# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    @api.multi
    def open_account_management(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'VITT Account Management',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'vitt_account_management.config_settings',
            'target': 'new',
        }


class ResCompany(models.Model):
    _inherit = 'res.company'

    property_account_receivable_id = fields.Many2one('account.account', string="Receivable Account", domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
                                                     help="This account will be used default")
    property_account_payable_id = fields.Many2one('account.account', string="Payable Account", domain="[('internal_type', '=', 'payable'), ('deprecated', '=', False)]",
                                                  help="This account will be used default")
    property_account_expense_categ_id = fields.Many2one('account.account', string='Expense Account on Category Product')
    property_account_income_categ_id = fields.Many2one('account.account', string='Income Account on Category Product')
    property_account_expense_id = fields.Many2one('account.account', string='Expense Account on Product Template')
    property_account_income_id = fields.Many2one('account.account', string='Income Account on Product Template')
    default_sale_tax_id = fields.Many2one('account.tax', string="Default Sale Tax", help="This sale tax will be assigned by default on new products.", oldname="default_sale_tax")
    default_purchase_tax_id = fields.Many2one('account.tax', string="Default Purchase Tax", help="This purchase tax will be assigned by default on new products.", oldname="default_purchase_tax")

    def generate_properties(self):
        self.ensure_one()
        PropertyObj = self.env['ir.property']
        todo_list = [
            ('property_account_receivable_id', 'res.partner', 'account.account'),
            ('property_account_payable_id', 'res.partner', 'account.account'),
            ('property_account_expense_categ_id', 'product.category', 'account.account'),
            ('property_account_income_categ_id', 'product.category', 'account.account'),
            ('property_account_expense_id', 'product.template', 'account.account'),
            ('property_account_income_id', 'product.template', 'account.account'),
            ('property_stock_account_input_categ_id', 'product.category', 'account.account'),
            ('property_stock_account_output_categ_id', 'product.category', 'account.account'),
            ('property_stock_valuation_account_id', 'product.category', 'account.account'),
        ]
        for record in todo_list:
            # take id of account
            account = getattr(self, record[0])
            value = account and 'account.account,' + str(account.id) or False
            if value:
                field = self.env['ir.model.fields'].search([('name', '=', record[0]), ('model', '=', record[1]), ('relation', '=', record[2])], limit=1)
                vals = {
                    'name': record[0],
                    'company_id': self.id,
                    'fields_id': field.id,
                    'value': value,
                }
                properties = PropertyObj.search([('name', '=', record[0]), ('res_id', '=', False), ('company_id', '=', self.id)])
                if properties:
                    # the property exist: modify it
                    properties.write(vals)
                else:
                    # create the property
                    PropertyObj.create(vals)
            else:
                # value
                properties = PropertyObj.search([('name', '=', record[0]), ('res_id', '=', False), ('company_id', '=', self.id)])
                if properties:
                    # delete
                    properties.unlink()
        return True

    @api.multi
    def set_product_taxes(self):
        """ Set the product taxes if they have changed """
        ir_values_obj = self.env['ir.values']
        if self.default_sale_tax_id:
            ir_values_obj.sudo().set_default('product.template', "taxes_id", [self.default_sale_tax_id.id], for_all_users=True, company_id=self.id)
        if self.default_purchase_tax_id:
            ir_values_obj.sudo().set_default('product.template', "supplier_taxes_id", [self.default_purchase_tax_id.id], for_all_users=True, company_id=self.id)

    @api.multi
    def write(self, vals):
        res = super(ResCompany, self).write(vals)
        self.generate_properties()
        self.set_product_taxes()

        return res


class account_management(models.TransientModel):
    _name = "vitt_account_management.config_settings"
    _inherit = 'res.config.settings'
    # _inherit = 'account.config.settings'

    # @api.model
    # def _default_account_payable(self):
    #     _logger.info("self.id " + str(self.id) + " SELF.ENV.USER.COMPANY_ID.ID " + str(self.env.user.company_id.id))
    #     account = ''
    #     company_id = self.env.user.company_id.id
    #     PropertyObj = self.env['ir.property']
    #     properties = PropertyObj.search([('name', '=', 'property_account_payable_id'), ('res_id', '=', False), ('company_id', '=', company_id)])
    #     if properties:
    #         value = properties.value_reference.split(',')
    #         account_id = int(value[1])
    #         accountobj = self.env['account.account']
    #         account = accountobj.search([('id', '=', account_id)])
    #     _logger.info("*"*10)
    #     _logger.info(str(account))
    #     # print "*"*10
    #     # print account
    #     return account

    company_id = fields.Many2one('res.company', string='Company', help='code of company', required=True, select=1, default=lambda self: self.env.user.company_id.id, readonly=True, oldname='company')
    property_account_receivable_id = fields.Many2one('account.account', related='company_id.property_account_receivable_id')
    property_account_payable_id = fields.Many2one('account.account', related='company_id.property_account_payable_id')
    property_account_expense_categ_id = fields.Many2one('account.account', related='company_id.property_account_expense_categ_id', help='This account will be used default when you create a New Product Category')
    property_account_income_categ_id = fields.Many2one('account.account', related='company_id.property_account_income_categ_id', help='This account will be used default when you create a New Product Category')
    property_account_expense_id = fields.Many2one('account.account', related='company_id.property_account_expense_id', help='This account will be used default when you create a New Product')
    property_account_income_id = fields.Many2one('account.account', related='company_id.property_account_income_id')
    property_stock_account_input_categ_id = fields.Many2one('account.account', related='company_id.property_stock_account_input_categ_id', help='This account will be used default when you create a New Product Category')
    property_stock_account_output_categ_id = fields.Many2one('account.account', related='company_id.property_stock_account_output_categ_id', help='This account will be used default when you create a New Product Category')
    property_stock_valuation_account_id = fields.Many2one('account.account', related='company_id.property_stock_valuation_account_id', help='This account will be used default when you create a New Product Category')
    transfer_account_id = fields.Many2one('account.account', related='company_id.transfer_account_id', domain=[('deprecated', '=', False)])
    income_currency_exchange_account_id = fields.Many2one('account.account', related='company_id.income_currency_exchange_account_id', domain=[('deprecated', '=', False)])
    expense_currency_exchange_account_id = fields.Many2one('account.account', related='company_id.expense_currency_exchange_account_id', domain=[('deprecated', '=', False)])
    chart_template_id = fields.Many2one('account.chart.template', related='company_id.chart_template_id')
    default_sale_tax_id = fields.Many2one('account.tax', related='company_id.default_sale_tax_id')
    default_purchase_tax_id = fields.Many2one('account.tax', related='company_id.default_purchase_tax_id')
    # default_sale_tax_id = fields.Many2one('account.tax', string="Default Sale Tax", help="This sale tax will be assigned by default on new products.", oldname="default_sale_tax")
    # default_purchase_tax_id = fields.Many2one('account.tax', string="Default Purchase Tax", help="This purchase tax will be assigned by default on new products.", oldname="default_purchase_tax")
