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
from odoo import models, fields, api, _
from odoo import http, _
from odoo.http import controllers_per_module
    
class PosClient_detail(models.Model):
    _inherit = 'res.users'
    
    @api.one
    def get_client_detail(self, args):
        print 'get_client_details :  ',args,args.get('session_id')
        
        print 'Context :::::::::::;;;;;;;  ',self._context
        if not args:
            args = {}
        if args.get('client_id'):
            user_datas = self.env['res.partner'].search([('id','=',args.get('client_id'))])
            args.update({'printer_config': self.printer_config,
                             'printer_port': self.printer_port,
                             'printer_model':self.printer_model,
                             'partner_afip_code':user_datas.partner_afip_code,
#                              'responsbility':user_datas
                             'partner_code':user_datas.partner_code,
                             'id_number':user_datas.id_numbers.name,
                             'customer_name':user_datas.name,
                             'main_id_number': user_datas.main_id_number,
                             'afip_responsability_type_id':user_datas.afip_responsability_type_id.name})
#             address=({
            customer_address1 = user_datas.street or ''
            customer_address2 = user_datas.street2 or ''
            city = user_datas.city or ''
            state = user_datas.state_id.name or ''
            zip = user_datas.zip or ''
            country = user_datas.country_id.name or ''
#                     })
            pos_session = self.env['pos.session'].search([('id','=',args.get('session_id'))])
#             print 'POS SESSSION DETAILS   :::::    ',pos_session.invoice_journal_id
#             print 'POS RECIEPT TYPE   :::::    ',pos_session.config_id.invoice_journal_id.name or 

            print 'JOURNAL ID ::::::------------------------',pos_session.config_id.invoice_journal_id
            for datas in pos_session.config_id.invoice_journal_id.journal_document_type_ids:
                print 'JOURNAL TYPES    :::  :::::::::::::: ',datas.document_type_id.name
                print 'Document Type ::::  :::::: ',datas.document_type_id.document_letter_id.name
                print 'Datas ::::   ',datas
            #journal_document_type_id
            address = str(customer_address1)+','+str(customer_address2)+','+str(city)+','+str(state)+','+str(country)+'-'+str(zip)
#             address = str(user_datas.street)+str(user_datas.street2)+str(user_datas.city)+str(user_datas.state_id.name)+str(user_datas.zip)+str(user_datas.country_id.name)
            args.update({'customer_address':address})
        return args
         
        
class Pospartner_detail(models.Model):
    _inherit = 'res.partner'
        
    partner_code = fields.Char(related='main_id_category_id.code',
                             string="Code")
        
    partner_afip_code = fields.Integer(related='main_id_category_id.afip_code',
                             string="AFIP_Code")
      
class Pos_order(models.Model):
    _inherit = "pos.order"
      
    receipt_number = fields.Char(string="POS Ticket No.")
    