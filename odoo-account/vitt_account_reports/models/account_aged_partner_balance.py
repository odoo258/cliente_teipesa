# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, date, timedelta


class report_account_aged_partner(models.AbstractModel):
    _inherit = 'account.aged.partner'

    @api.model
    def _lines(self, context, line_id=None):
        lines = super(report_account_aged_partner, self)._lines(context)

        for line in lines:
            ref = ""
            dt = ""
            level_l = line.get("level")
            type_l = line.get("type")
            if (level_l == 1) and (type_l == "move_line_id"):
                move_line_id = line.get("id")
                domain = [('id', '=', move_line_id)]
                move_line = self.env['account.move.line'].search(domain, limit=1)
                if move_line:
                    if move_line.invoice_id.date_invoice:
                        dt = move_line.invoice_id.date_invoice

                    if move_line.invoice_id.type == "in_invoice":
                        ref = move_line.invoice_id.reference

            name = line.get("name")
            new_name = ref or name
            # if ref:
            #     new_name = ref

            if dt:
                dt = "%s: %s" % (_("Date"), dt)
                new_name = "%s %s" % (new_name, dt)

            line.update({"name": new_name})

        return lines
