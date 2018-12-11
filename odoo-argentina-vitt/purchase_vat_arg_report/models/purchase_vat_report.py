# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from odoo import models, fields, api, _
from odoo.tools.misc import formatLang
from datetime import datetime, timedelta
from odoo.tools.safe_eval import safe_eval


class report_account_purchase_vat_report(models.AbstractModel):
    _name = "purchase.vat.report"
    _description = "Purchase VAT Report"
    
    
    def _format(self, value, currency=False):
        if self.env.context.get('no_format'):
            return value
        currency_id = currency or self.env.user.company_id.currency_id
        if currency_id.is_zero(value):
            value = abs(value)
        res = formatLang(self.env, value, currency_obj=currency_id)
        return res
    
    @api.model
    def get_lines(self, context_id, line_id=None):
        if type(context_id) == int:
            context_id = self.env['account.context.purchase.report'].search([['id', '=', context_id]])
        new_context = dict(self.env.context)
        new_context.update({
            'date_from': context_id.date_from,
            'date_to': context_id.date_to,
            'state': context_id.all_entries and 'all' or 'posted',
            'cash_basis': context_id.cash_basis,
            'context_id': context_id,
            'company_ids': context_id.company_ids.ids,
            'journal_purchase_ids': context_id.journal_purchase_ids.ids,
        })
        return self.with_context(new_context)._lines(line_id)
    
    @api.model
    def _lines(self, line_id=None):
        ctx = self._context 
        lines = []
        name = 0
        doc_latter_name = ''
        
        context = self.env.context
        company_id = context.get('company_id') or self.env.user.company_id
        search_invoice = self.env['account.invoice'].search(['|',('type','=', 'in_invoice'),('type','=', 'in_refund'),('state','!=', 'draft'),('state','!=', 'cancel'),('date_invoice','>=', ctx.get('date_from')),('date_invoice','<=', ctx.get('date_to')) ])
        for inv in search_invoice:
            name += 1
            total_vat_perception = total_gross_income_perception = total_exempt = total_no_vat = total_vat = total_all_amount = total_base_amount=  0.00
            doc_latter_name = str(inv.document_letter_id.name) + " " + str(inv.display_name)
            lines.append({
                'id': inv.id,
                'type': 'line',
                'name': name,
                'footnotes': self.env.context['context_id']._get_footnotes('line', inv.id),
                'level': 2,
                'columns': [ inv.date_invoice , doc_latter_name , inv.journal_document_type_id.document_type_id.name , inv.partner_id.afip_responsability_type_id.name , inv.partner_id.main_id_number , inv.partner_id.name],
            })
            lines.append({
                    'id': 0,
                    'type': 'line_header',
                    'name':'% IVA',
                    'footnotes': {},
                    'columns': ['Monto Base', 'Percepcion IVA', 'IIBB', 'Exento', 'No Grabado' ,'IVA' ,'Total'],
                    'level': 1,
                   
                })
            for a in inv.tax_line_ids:
                amount = 0
                company_currency = inv.currency_id.with_context(date=inv.date_invoice)
                com_currency = inv.company_id.currency_id
                if company_currency != com_currency:
                    amt = a.amount or a.base
                    amount = company_currency.compute(amt,com_currency)
                base = vat_perception = gross_income_perception = exempt = no_vat = vat = total_amount = 0
                if a.tax_id.tax_group_id.tax == 'vat' and a.tax_id.tax_group_id.type == 'tax'  and a.tax_id.tax_group_id.afip_code in [3, 4, 5, 6, 8, 9]:
                    amount2 = 0
                    if company_currency != com_currency:
                        amt2 = a.base
                        amount2 = company_currency.compute(amt2, com_currency)
                    if amount2:
                        base = amount2
                    else:
                        base = a.base
                if a.tax_id.tax_group_id.tax == 'vat' and a.tax_id.tax_group_id.type == 'perception':
                    if amount:
                        vat_perception = amount
                    else:
                        vat_perception = a.amount or a.base
                if a.tax_id.tax_group_id.tax == 'gross_income' and a.tax_id.tax_group_id.type == 'perception':
                    if amount:
                        gross_income_perception = amount
                    else:
                        gross_income_perception = a.amount or a.base
                if a.tax_id.tax_group_id.tax == 'vat' and a.tax_id.tax_group_id.type == 'tax' and a.tax_id.tax_group_id.afip_code == 2:
                    if amount:
                        exempt = amount
                    else:
                        exempt = a.amount or a.base
                if a.tax_id.tax_group_id.tax == 'vat' and a.tax_id.tax_group_id.type == 'tax' and a.tax_id.tax_group_id.afip_code == 1:
                    if amount:
                        no_vat = amount
                    else:
                        no_vat = a.amount or a.base
                if a.tax_id.tax_group_id.tax == 'vat' and a.tax_id.tax_group_id.type == 'tax' and a.tax_id.tax_group_id.afip_code in [4,5,6,8,9]:
                    if amount:
                        vat = amount
                    else:
                        vat = a.amount or a.base  
                total_amount = base+vat_perception + gross_income_perception + exempt + no_vat +vat
                total_vat_perception += vat_perception 
                total_gross_income_perception += gross_income_perception
                total_exempt += exempt
                total_no_vat += no_vat
                total_vat += vat
                total_all_amount += total_amount
                total_base_amount += base 
                lines.append({
                'id': a.id,
                'type': 'line',
                'name': a.name ,
                'footnotes': self.env.context['context_id']._get_footnotes('line', a.id),
                'level': 1,
                'columns': [ base , vat_perception , gross_income_perception , exempt , no_vat ,vat,total_amount],
            })
            lines.append({
                'id': 0,
                'type': 'total',
                'name': _('Total'),
                'footnotes': {},
                'level': 0,
                  'unfoldable': False,
                'unfolded': False,
                'columns': [ total_base_amount ,total_vat_perception , total_gross_income_perception, total_exempt , total_no_vat ,total_vat,total_all_amount],
            })
            
        return lines
    
    @api.model
    def get_title(self):
        return _("Libro IVA Compras (Argentina)")
    
    @api.model
    def get_name(self):
        return 'purchase_vat_report'
        
    @api.model
    def get_report_type(self):
        return self.env.ref('purchase_vat_arg_report.bi_account_report_type_purchase_vat')
    
    def get_template(self):
        return 'account_reports.report_financial'
 
        
class account_context_purchase_report(models.TransientModel):
    _name = "account.context.purchase.report"
    _description = "A particular context for the purchase"
    _inherit = "account.report.context.common"

    fold_field = 'unfolded_invoice'
    unfolded_invoice = fields.Many2many('account.invoice','invoice_report_rel','invoice_id','report_id', string='Unfolded lines')
    journal_purchase_ids = fields.Many2many('account.journal', relation='account_report_purchase_journals')
    available_purchase_journal_ids = fields.Many2many('account.journal', relation='account_report_purchase_available_journal', default=lambda s: [(6, 0, s.env['account.journal'].search([]).ids)])
    
    
    @api.multi
    def get_available_journal_ids_names_and_codes_purchase(self):
        journal = self.env['account.journal'].search([])
        journal_ids = [[c.id, c.name, c.code] for c in journal]
        return journal_ids

    @api.model
    def get_available_journals(self):
        return self.env.user.journal_purchase_ids
    
    
    def get_report_obj(self):
        return self.env['purchase.vat.report']

    def get_columns_names(self):
        return [_("Invoice Date"),_("Invoice Official No."), _("Document Type"), _("VAT Responsibility"), _("CUIT/CUIL Supplier"), _("Supplier Name"),_(" ")]

    @api.multi
    def get_columns_types(self):
        return ["date", "text", "text", "text", "text", "text","text"]

    
    
class account_context_inherit(models.TransientModel):
    _inherit = "account.report.context.common"
    
    
    '''@api.multi
    def get_available_tax_ids_and_names(self):
        tax_ids = self.env['account.tax']
        return [[c.id, c.name] for c in tax_ids]

    @api.model
    def get_available_taxes(self):
        return self.env.user.tax_ids'''
    
    def _report_name_to_report_model(self):
        return {
            'financial_report': 'account.financial.html.report',
            'generic_tax_report': 'account.generic.tax.report',
            'followup_report': 'account.followup.report',
            'bank_reconciliation': 'account.bank.reconciliation.report',
            'general_ledger': 'account.general.ledger',
            'aged_receivable': 'account.aged.receivable',
            'aged_payable': 'account.aged.payable',
            'coa': 'account.coa.report',
            'l10n_be_partner_vat_listing': 'l10n.be.report.partner.vat.listing',
            'l10n_be_partner_vat_intra': 'l10n.be.report.partner.vat.intra',
            'partner_ledger': 'account.partner.ledger',
            'purchase_vat_report':'purchase.vat.report',
        }

    def _report_model_to_report_context(self):
        return {
            'account.financial.html.report': 'account.financial.html.report.context',
            'account.generic.tax.report': 'account.report.context.tax',
            'account.followup.report': 'account.report.context.followup',
            'account.bank.reconciliation.report': 'account.report.context.bank.rec',
            'account.general.ledger': 'account.context.general.ledger',
            'account.aged.receivable': 'account.context.aged.receivable',
            'account.aged.payable': 'account.context.aged.payable',
            'account.coa.report': 'account.context.coa',
            'l10n.be.report.partner.vat.listing': 'l10n.be.partner.vat.listing.context',
            'l10n.be.report.partner.vat.intra': 'l10n.be.partner.vat.intra.context',
            'account.partner.ledger': 'account.partner.ledger.context',
            'purchase.vat.report': 'account.context.purchase.report',
        }
        
    
    '''@api.multi
    def get_html_and_data(self, given_context=None):
        if given_context is None:
            given_context = {}
        result = {}
        if given_context:
            if 'force_account' in given_context and (not self.date_from or self.date_from == self.date_to):
                self.date_from = self.env.user.company_id.compute_fiscalyear_dates(datetime.strptime(self.date_to, "%Y-%m-%d"))['date_from']
                self.date_filter = 'custom'
        lines = self.get_report_obj().get_lines(self)
        rcontext = {
            'res_company': self.env['res.users'].browse(self.env.uid).company_id,
            'context': self,
            'report': self.get_report_obj(),
            'lines': lines,
            'footnotes': self.get_footnotes_from_lines(lines),
            'mode': 'display',
        }
        result['html'] = self.env['ir.model.data'].xmlid_to_object(self.get_report_obj().get_template()).render(rcontext)
        result['report_type'] = self.get_report_obj().get_report_type().read(['date_range', 'comparison', 'cash_basis', 'tax','analytic', 'extra_options'])[0]
        select = ['id', 'date_filter', 'date_filter_cmp', 'date_from', 'date_to', 'periods_number', 'date_from_cmp', 'date_to_cmp', 'cash_basis', 'all_entries', 'company_ids', 'multi_company', 'hierarchy_3', 'analytic']
        if self.get_report_obj().get_name() == 'general_ledger':
            select += ['journal_ids']
            result['available_journals'] = self.get_available_journal_ids_names_and_codes()
            
        if self.get_report_obj().get_name() == 'purchase_vat_report':
            select += ['journal_purchase_ids']
            result['available_journals'] = self.get_available_journal_ids_names_and_codes_purchase()
        if self.get_report_obj().get_name() == 'partner_ledger':
            select += ['account_type']
        result['report_context'] = self.read(select)[0]
        result['report_context'].update(self._context_add())
        if result['report_type']['analytic']:
            result['report_context']['analytic_account_ids'] = [(t.id, t.name) for t in self.analytic_account_ids]
            result['report_context']['analytic_tag_ids'] = [(t.id, t.name) for t in self.analytic_tag_ids]
            result['report_context']['available_analytic_account_ids'] = self.analytic_manager_id.get_available_analytic_account_ids_and_names()
            result['report_context']['available_analytic_tag_ids'] = self.analytic_manager_id.get_available_analytic_tag_ids_and_names()
        result['xml_export'] = self.env['account.financial.html.report.xml.export'].is_xml_export_available(self.get_report_obj())
        result['fy'] = {
            'fiscalyear_last_day': self.env.user.company_id.fiscalyear_last_day,
            'fiscalyear_last_month': self.env.user.company_id.fiscalyear_last_month,
        }
        result['available_companies'] = self.multicompany_manager_id.get_available_company_ids_and_names()
        result['available_taxes'] = self.get_available_tax_ids_and_names()
        return result'''
