# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################
from odoo import models, fields, api, exceptions
from odoo.tools.translate import _


class invoice_merge(models.TransientModel):
    _name = "invoice.merge"
    _description = "Merge Partner Invoice"

    keep_references = fields.Boolean('Keep references'
                                     ' from original invoices',
                                     default=True)
    date_invoice = fields.Date('Invoice Date')

    @api.model
    def _dirty_check(self):
        if self.env.context.get('active_model', '') == 'account.invoice':
            ids = self.env.context['active_ids']
            if len(ids) < 2:
                raise exceptions.Warning(
                    _('Please select multiple invoice to merge in the list '
                      'view.'))
            inv_obj = self.env['account.invoice']
            invs = inv_obj.read(ids,
                                ['account_id', 'state', 'type', 'company_id',
                                 'partner_id', 'currency_id', 'journal_id'])
            for d in invs:
                if d['state'] != 'draft':
                    raise exceptions.Warning(
                        _('At least one of the selected invoices is %s!') %
                        d['state'])
                if d['account_id'] != invs[0]['account_id']:
                    raise exceptions.Warning(
                        _('Not all invoices use the same account!'))
                if d['company_id'] != invs[0]['company_id']:
                    raise exceptions.Warning(
                        _('Not all invoices are at the same company!'))
                if d['partner_id'] != invs[0]['partner_id']:
                    raise exceptions.Warning(
                        _('Not all invoices are for the same partner!'))
                if d['type'] != invs[0]['type']:
                    raise exceptions.Warning(
                        _('Not all invoices are of the same type!'))
                if d['currency_id'] != invs[0]['currency_id']:
                    raise exceptions.Warning(
                        _('Not all invoices are at the same currency!'))
                if d['journal_id'] != invs[0]['journal_id']:
                    raise exceptions.Warning(
                        _('Not all invoices are at the same journal!'))
        return {}

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(invoice_merge, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=False)
        self._dirty_check()
        return res

    @api.multi
    def merge_invoices(self):
        inv_obj = self.env['account.invoice']
        inv_obj_line = self.env["account.invoice.line"]
        aw_obj = self.env['ir.actions.act_window']
        ids = self.env.context.get('active_ids', [])
        invoices = inv_obj.browse(ids)
        reference = ""
        invoice = inv_obj.browse(ids)[0]
        vals_invoice = {
            'partner_id': invoice.partner_id.id,
            'journal_id': invoice.journal_id.id,
            'date_invoice': self.date_invoice,
            'user_id': invoice.user_id.id,
            'currency_id': invoice.currency_id.id,
            'company_id': invoice.company_id.id,
            'type': invoice.type,
            'account_id': invoice.account_id.id,
            'state': 'draft',
            'comment': invoice.comment,
            'payment_term_id': invoice.payment_term_id.id,
            'invoice_line_ids': {},
        }
        invoice_id = inv_obj.create(vals_invoice)
        invoice_line_id = []
        inv = []
        if invoice_id:
            inv.append(invoice_id.id)
            vals = {}
            product_id = []
            for invs in invoices:
                for lines in invs.invoice_line_ids:
                    vals["product_id"] = lines.product_id.id
                    vals['name'] = lines.name
                    vals['price_unit'] = lines.price_unit
                    vals["origin"] = lines.origin
                    vals["account_id"] = lines.account_id.id
                    # vals["invoice_line_tax_ids"] = lines.invoice_line_tax_ids.id
                    vals["account_analytic_id"] = lines.account_analytic_id.id
                    vals["discount"] = lines.discount
                    vals["asset_category_id"] = lines.asset_category_id.id
                    vals["uom_id"] = lines.uom_id.id
                    vals["quantity"] = lines.quantity
                    vals["invoice_id"] = invoice_id.id
                    # != lines.product_id.id:
                    if lines.product_id.id not in product_id:
                        product_id.append(lines.product_id.id)
                        line_id = inv_obj_line.create(vals)
                        if line_id:
                            invoice_line_id.append(line_id.id)
                            if lines.invoice_line_tax_ids:
                                for tax in lines.invoice_line_tax_ids:
                                    line_id.write({'invoice_line_tax_ids': [(4, tax.id, None)]})
                    else:
                        obj_line = self.env["account.invoice.line"].search([('id', 'in', tuple(invoice_line_id)), ('discount', '=', lines.discount), ('price_unit', '=', lines.price_unit), ('asset_category_id', '=', lines.asset_category_id.id), ('name', '=', lines.name), ('product_id', '=', lines.product_id.id)])
                        if obj_line:
                            values = {'quantity': obj_line.quantity + lines.quantity, }
                            obj_line.write(values)
                        else:
                            line_id = inv_obj_line.create(vals)
                            for tax in lines.invoice_line_tax_ids:
                                line_id.write({'invoice_line_tax_ids': [(4, tax.id, None)]})
        if not invoice_line_id:
            invoice_id.unlink()
        else:
            for invoice_state in invoices:
                if invoice_state.origin:
                    if reference:
                        reference = reference + ", " + invoice_state.origin
                    else:
                        reference = invoice_state.origin
                invoice_state.write({'state': 'cancel'})
                invoice_id.write({'name': reference, 'origin': reference})
            invoice_id.compute_taxes()

        xid = {
            'out_invoice': 'action_invoice_tree1',
            'out_refund': 'action_invoice_tree3',
            'in_invoice': 'action_invoice_tree2',
            'in_refund': 'action_invoice_tree4',
        }[invoices[0].type]

        action = aw_obj.for_xml_id('account', xid)
        action.update({
            'domain': [('id', 'in', ids + inv)],
        })
        return action
