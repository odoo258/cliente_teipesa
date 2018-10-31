# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import UserError


class AfipWsConsultWizard(models.TransientModel):
    _name = 'afip.ws.consult.wizard'
    _description = 'AFIP WS Consult Wizard'

    number = fields.Integer(
        'Number',
        required=True,
    )

    @api.multi
    def confirm(self):
        self.ensure_one()
        journal_document_type_id = self._context.get('active_id', False)
        if not journal_document_type_id:
            raise UserError(_(
                'No Journal Document Class as active_id on context'))
        journal_document_type = self.env[
            'account.journal.document.type'].browse(
            journal_document_type_id)
        return journal_document_type.get_pyafipws_consult_invoice(self.number)
