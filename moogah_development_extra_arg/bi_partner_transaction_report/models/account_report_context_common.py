# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##################################################################################

from odoo import models, fields, api, _
from odoo.tools.misc import formatLang
from datetime import datetime, timedelta
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
from operator import itemgetter


class AccountReportContextCommon(models.TransientModel):
    _inherit = "account.report.context.common"
    
    def _report_name_to_report_model(self):
        res = super(AccountReportContextCommon, self)._report_name_to_report_model()
        res.update({'vendor_transaction_report': 'vendor.transaction.report',
                    'partner_transaction_report': 'partner.transaction.report',
                    'currencies_customer_ledger_report':'currencies.customer.ledger.report',
                    'currencies_vendor_ledger_report':'currencies.vendor.ledger.report'})
        return res


    def _report_model_to_report_context(self):
        res = super(AccountReportContextCommon, self)._report_model_to_report_context()
        res.update({'partner.transaction.report': 'partner.transection.context.report',
                    'vendor.transaction.report': 'vendor.transection.context.report',
                    'currencies.customer.ledger.report': 'currencies.customer.ledger.context.report',
                    'currencies.vendor.ledger.report': 'currencies.vendor.ledger.context.report'})
        return res

