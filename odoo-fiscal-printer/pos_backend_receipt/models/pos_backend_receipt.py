# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2017 OpenERP SA (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
import sets
import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'
    ip_address = fields.Char(string='IP address')
    printer_port=fields.Char(string='Printer Port',required = True)
    printer_config = fields.Selection([('argentina', 'Argentina'),('chile','Chile'), ('panama', 'Panama')], string='Printer Country', default='argentina',required = True)
    printer_model = fields.Char(string='Printer Model',required = True)
    
    @api.multi
    def get_user_ip_address(self):
        ip_address = False
        if self._uid:
            ip_address = self.browse(self._uid).ip_address or False
        return ip_address


class res_partner(models.Model):
    _inherit = 'account.invoice'
    isValidateFiscal=fields.Boolean(string='FiscalValidate')
    regTaxNumber = ''

    @api.multi
    def copy(self, default=None):
        # self.ensure_one()
        print 'DUPLICATE RECORD CAN NOT BE GENERATED.'
        raise Warning('You cannot create duplicate.')

    @api.multi
    def get_printer_data(self,type):
       if type=="printer":
        list3=[]
        for invoice_rec in self:

            if not invoice_rec.isValidateFiscal:
                list1=[]
                autovalidate = invoice_rec.action_invoice_open()
                invoice_rec.isValidateFiscal=True
                print 'ACCOUNT_INVOICE.......................',autovalidate
                account_dict={
                                'report':'accountinovice',
                                'type':self.type,
                                'customer_name':invoice_rec.partner_id.name or '',
                                'company':invoice_rec.partner_id.parent_id.name or '',
                                'address':invoice_rec.partner_id.street or '',
                                'zip':invoice_rec.partner_id.zip or '',
                                'city':invoice_rec.partner_id.city or '',
                                'country': invoice_rec.partner_id.country_id.name or '',
                                'number':invoice_rec.number or 0000,
                                'invoice_date':invoice_rec.date_invoice or 0,
                                'Salesperson':invoice_rec.user_id.name or 0,

                                # Document Type
                                'IsPerception':invoice_rec.document_type_id.name or  '',
                                'PaymentTerms':invoice_rec.payment_term_id.name or 0,
                                'receipt_type':invoice_rec.document_type_id and invoice_rec.document_type_id.document_letter_id.name or '',

                                # COMMENTING CODE
                                'RegTaxNumber':invoice_rec.partner_id.id_numbers.name or '0',
                                'DocumentName':str(invoice_rec.document_type_id.name) or '',
                                'InvoiceType':invoice_rec.partner_id.afip_responsability_type_id.name or '',
                                'IsCreditInovice':invoice_rec.document_type_id.internal_type or '',
                                'DocumentCode':invoice_rec.partner_id.id_numbers.category_id.code or '',

                                #TOTAL
                                'amount_total':invoice_rec.amount_total or '0',

                                #INVOICE NUMBER
                                'InvoiceNumber':invoice_rec.document_number or '',

                                #AFIP_RESPOSIBILITY TYPE
                                'AFIPResId':invoice_rec.afip_responsability_type_id.code or '',
                              }
                account_dict.update({'AFIPNUMBER':invoice_rec.partner_id.main_id_category_id.code or '',})
                if invoice_rec.partner_id.main_id_category_id.code == 'CUIT':
                    try:
                        account_dict.update({'AFIPcode':invoice_rec.partner_id.id_numbers.afip_code or 00000})
                    except:
                        pass


                print 'TOTAL : -----------------------------------------------------',invoice_rec.amount_total or '0'
                for invoice_line_rec in invoice_rec.invoice_line_ids:
                    product_name = invoice_line_rec.product_id.name or 0
                    quantity = invoice_line_rec.quantity or 0
                    price= invoice_line_rec.price_unit or 0
                    discount=invoice_line_rec.discount or 0
                    for taxs in invoice_line_rec.invoice_line_tax_ids:
                        if taxs.tax_group_id.type == 'perception':
                            tax = taxs.amount or 0
                            if abs(discount):
                                percept_amount=(float(price*quantity) - float(price*quantity*(float(discount/100.00))))*(float(taxs.amount)/100.00)
                                print 'PERCEPTION AMOUNT :------------------------------------------------------------',percept_amount
                                percept_Unit = "%0.2f"%(percept_amount)
                                # percept_Unit = float(str(percept_amount).split(".")[0] + "." + "%0.3s" % (str(percept_amount).split(".")[-1]))
                                print 'PERCEPT UNIT :------------------------------------------------------------------',percept_Unit
                                dict11={'receipttype':'perception',
                                        'percpt_text':taxs.name,
                                        'percpt_amount':float(percept_Unit),
                                        'percpt_tax': float(tax),
                                        }
                            else:
                                percept_amount=float(price*quantity*(float(taxs.amount)/100.00))
                                percept_Unit = "%0.2f"%(percept_amount)
                                print 'PERCEPTION AMOUNT :------------------------------------------------------------',percept_amount
                                # percept_Unit = float(str(percept_amount).split(".")[0] + "." + "%0.3s" % (str(percept_amount).split(".")[-1]))
                                print 'PERCEPT UNIT :------------------------------------------------------------------',percept_Unit
                                dict11={
                                        'receipttype':'perception',
                                        'percpt_text':taxs.name,
                                        'percpt_amount':float(percept_Unit),
                                        'percpt_tax': float(tax),
                                        }
                            list3.append(dict11)
                        else:
                            dict1={
                              'product':product_name or 0,
                              'quantity':quantity or 0,
                              'price':price or 0,
                              'discount':discount or 0,
                              'tax':(taxs.amount) or 0
                               }
                            list1.append(dict1)

                list2=[]
                org_price =invoice_rec.amount_untaxed
                tax_price=invoice_rec.amount_tax
                total=invoice_rec.amount_total
                dict2={'Orgprice':org_price or 0,
                       'taxprice':tax_price or 0,
                       'total':round(total,2)
                       }
                account_dict.update(dict2)
                account_dict.update({'product':list1})
                if list3:
                    account_dict.update({"perception":list3})
                return [account_dict,self.env['res.users'].get_user_ip_address(), self.env.user.printer_config, self.env.user.printer_port,self.env.user.printer_model]

            else:
                raise Warning('You cannot print more than 1 times.')
            # if not invoice_rec.isValidateFiscal
       # TO AUTO CANCEL
       elif type == "auto_cancel":
            account_dict={'report':'autocancelreceipt',}
            return [account_dict,self.env['res.users'].get_user_ip_address(), self.env.user.printer_config, self.env.user.printer_port,self.env.user.printer_model]

       # TO REPORT Z 
       elif type == "report_z":
            account_dict={'report':'closingfiscalz',}
            return [account_dict,self.env['res.users'].get_user_ip_address(), self.env.user.printer_config, self.env.user.printer_port,self.env.user.printer_model]

       # TO REPORT X
       elif type == "report_x":
            account_dict={'report':'closingfiscalx',}
            return [account_dict,self.env['res.users'].get_user_ip_address(), self.env.user.printer_config, self.env.user.printer_port,self.env.user.printer_model]
       else:
            _logger.warning("Unknown button type")   
