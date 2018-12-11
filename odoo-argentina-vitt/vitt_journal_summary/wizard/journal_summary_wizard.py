from datetime import datetime
from dateutil import relativedelta
from odoo import http, models, fields, api, _
import xlwt
from cStringIO import StringIO
import base64
from odoo import conf
import imp
from decimal import *
import copy
from dateutil import parser

TWOPLACES = Decimal(10) ** -2

def MultiplybyRate(rate, amountincur, curcomp, invcur):
    if curcomp != invcur:
        return rate * amountincur
    else:
        return amountincur

class ExcelExtendedJournal(models.TransientModel):
    _name= "excel.extended.journal"
    excel_file = fields.Binary('Download report Excel')
    file_name = fields.Char('Excel File', size=64)

class JournalAccountWiz(models.TransientModel):
    _name = 'journal.account.wiz'

    date_from = fields.Date(string='Date From', required=True,
        default=datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    legal_no = fields.Integer(string="Legal Ser. No.",translate=True,default="1")
    cust_inv = fields.Boolean(string="Customer Invoices",default=True)
    vend_inv = fields.Boolean(string="Vendor Bills",default=True)
    payments = fields.Boolean(string="Payments",default=True)
    receipts = fields.Boolean(string="Receipts",default=True)
    sort_by = fields.Selection(
        [('number','Number'),
        ('date','Journal Entry Date'),
        ('monthly','Monthly summary')],
        'Sort By',
        default='monthly',
        translate=True
    )

    @api.multi
    def ex_journalsummary(self):
        datas = {
            'date_froms': self.date_from,
            'date_tos': self.date_to,
            'legal_no': self.legal_no,
            'cust_inv': self.cust_inv,
            'vend_inv': self.vend_inv,
            'payments': self.payments,
            'receipts': self.receipts,
            'sort_by': self.sort_by
        }
        return self.env['report'].with_context(landscape=True).get_action(self, 'vitt_journal_summary.journalsummary', data=datas)


class report_journal_summary(models.Model):
    _name = "report.vitt_journal_summary.journalsummary"

    def GetPeriods(self,froms="",tos=""):
        years = int(parser.parse(tos).strftime('%Y')) - int(parser.parse(froms).strftime('%Y'))
        tom = int(parser.parse(tos).strftime('%m')) + (int(years)*12)
        fromm = int(parser.parse(froms).strftime('%m'))
        return  tom - fromm + 1

    def render_html(self,docids, data=None):
        periods = self.GetPeriods(data['date_froms'],data['date_tos'])

        domain = [('date', '>=', data['date_froms']), ('date', '<=', data['date_tos'])]
        moveModel = self.env['account.move']
        moveline = self.env['account.move.line']
        if data['sort_by'] == 'number':
            order_ = "name"
        if data['sort_by'] == 'date':
            order_ = "date"
        if data['sort_by'] == 'monthly':
            order_ = "date"
        moves = moveModel.search(domain,order=order_)
        for move in moves:
            moveline += move.line_ids
            # if move.document_type_id.internal_type not in ['customer_payment','supplier_payment','inbound_payment_voucher','outbound_payment_voucher']:
            #     moveline += move.line_ids
            # else:
            #     pass

        columns = [_('No'),_('Date'),_('Comment'),_(''),_('Reference'),_('Account'),_(''),_('Description'),_('Debit'),_('Credit')]

        docargs = {
            'docs': moveline,
            'legal_no': data['legal_no'],
            'cust_inv': data['cust_inv'],
            'vend_inv': data['vend_inv'],
            'payments': data['payments'],
            'receipts': data['receipts'],
            'sort_by': data['sort_by'],
            'columns': columns
        }
        return self.env['report'].render('vitt_journal_summary.journalsummary', docargs)

class def_report_journal_summary(models.Model):
    _inherit = "account.move.line"


