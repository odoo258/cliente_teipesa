# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

'''
# no needed in v10
from odoo import models, fields, api
from odoo.osv import osv
import logging
_logger = logging.getLogger(__name__)

class base_language_install(osv.osv_memory):
    _inherit = 'base.language.install'
    new_languages=[('es_HN', 'Español HN / Español HN'),
                   ('es_NI', 'Español NI / Español NI'),
                   ('es_SV', 'Español SV / Español SV'),
                  ]
    lang = fields.Selection(selection_add=new_languages)
'''
