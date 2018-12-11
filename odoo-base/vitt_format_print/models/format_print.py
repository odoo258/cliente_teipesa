# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError, Warning, ValidationError
from odoo.tools import append_content_to_html, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from .. import utils
import base64
import os
import glob
import os.path


COLOR_LIST = utils.COLOR_LIST


class FormatPrint(models.Model):
    _name = 'format.print'

    @api.model
    def _get_report_paperformat_id(self):
        xml_id = self.env['ir.actions.report.xml'].search([('report_name', '=',
                                                            'vitt_format_print.format_print_template')])
        if not xml_id or not xml_id.paperformat_id:
            raise Warning('Someone has deleted the reference paperformat of report.Please Update the module!')
        return xml_id.paperformat_id.id

    def _fill_main_models(self):
        res = []
        domain = [('model_name', '!=', '')]
        main_models = self.env['format.print.main_models'].search(domain)
        for main_model in main_models:
            foundf = False
            for r in res:
                if r[0] == main_model.model_name:
                    foundf = True
                    break

            if not foundf:
                res.append((main_model.model_name, main_model.name))
        res.append(('no_model', 'No Model'))

        return res

    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.user.company_id)
    paper_format_id = fields.Many2one('report.paperformat', string="Paper Format", default=_get_report_paperformat_id)
    name = fields.Char(string="Format Print")
    user_ids = fields.Many2many("res.users", string="Users", help='Select the users who can print this format')
    # main_model = fields.Selection([('no_model', 'No Model'), ('other', 'Other Model')], string='Main Model', required=True)
    main_model = fields.Selection(selection=_fill_main_models, string='Main Model', required=True)
    main_model_id = fields.Many2one('format.print.main_models', string='Main Model')
    states = fields.Char(string='States')

    # page Height-Width Configuration
    page_height = fields.Float(string="Page Height (mm)", default=279)
    page_width = fields.Float(string="Page Width (mm)", default=216)
    arguments_line_ids = fields.One2many(
        'format.arguments.lines',
        'format_id',
        string='Print Arguments',
    )
    copies_line_ids = fields.One2many(
        'format.copies.lines',
        'format_id',
        string='Copies',
    )

    @api.onchange("main_model_id", )
    def _onchange_main_model_id(self):
        if self.main_model_id:
            self.main_model = self.main_model_id.model_name


class FormatCopiesLines(models.Model):
    _name = 'format.copies.lines'
    _description = 'Format Copies'

    format_id = fields.Many2one('format.print', string='Format', required=True)
    name = fields.Char(string="Copy Name", translate=True)
    description = fields.Char(string="Description", translate=True)


class FormatArgumentLines(models.Model):
    _name = 'format.arguments.lines'
    _description = 'Arguments in Format'

    def _fill_child_models(self):
        res = []
        domain = [('model_name', '!=', '')]
        child_models = self.env['format.print.child_models'].search(domain)
        for child_model in child_models:
            foundf = False
            for r in res:
                if r[0] == child_model.model_name:
                    foundf = True
                    break

            if not foundf:
                res.append((child_model.model_name, child_model.name))
        res.append(('no_model', 'No Model'))

        return res

    def _default_format_date(self):
        user = self.env['res.users'].browse(self.env.uid)
        lang = user.lang or 'en_US'
        lang_ids = self.env['res.lang'].search([('code', '=', lang)], limit=1)
        date_format = lang_ids.date_format or DEFAULT_SERVER_DATE_FORMAT

        return date_format

    def _get_default_from_model(self):
        mm = self._context.get('main_model')
        return mm

    def _get_default_from_model_id(self):
        fm = None
        mm = self._context.get('main_model_id')
        domain = [('main_model_id', '=', mm)]
        try:
            child_model = self.env['format.print.child_models'].search(domain, limit=1)
        except:
            child_model = {}
        if child_model:
            fm = child_model.id
        return fm

    def _get_default_main_model_id(self):
        mm = self._context.get('main_model_id')
        return mm

    name = fields.Char(string="Format Line")
    main_model = fields.Selection(related='format_id.main_model', readonly=True)
    format_id = fields.Many2one('format.print', string='Format', required=True)
    from_model = fields.Selection(selection=_fill_child_models, string='From Model', required=True, default=_get_default_from_model)
    # from_model = fields.Selection([('no_model', 'No Model'), ('other', 'Other Model')], string='From Model', required=True, default=_get_default_from_model)
    from_model_id = fields.Many2one('format.print.child_models', string='From Model', default=_get_default_from_model_id)
    main_model_id = fields.Many2one('format.print.main_models', default=_get_default_main_model_id)
    is_matrix = fields.Boolean(string='Is Matrix')
    matrix_field = fields.Char(string='Matrix Field')
    arguments = fields.Selection('_arguments', string='Argument', default='other_field', required=True)
    other_field = fields.Char(string='Field Name')
    other_text = fields.Char(string='Text', translate=True)
    image = fields.Binary('Image', attachment=True,
                          help="This field holds the image used as photo for the group, limited to 1024x1024px.")
    image_field = fields.Char(string='Image Field')
    argument_type = fields.Selection('_arguments_type', string='Argument Type', default='text',)
    format_date = fields.Char(string='Format Date', default=_default_format_date)
    format_number = fields.Selection('_format_number', string='Format number', default='number')

    # position
    top_margin = fields.Float(string="Top Margin (Y)")
    top_unit = fields.Selection('_units', string='Unit Measure', default="mm")
    left_margin = fields.Float(string="Left Margin (X)")
    left_unit = fields.Selection('_units', string='Unit Measure', default="mm")
    width = fields.Float(string="Width")
    width_unit = fields.Selection('_units', string='Unit Measure', default="mm")
    width_f = fields.Boolean(string='Use Width')
    height = fields.Float(string="Height (Z)")
    height_f = fields.Boolean(string='Use Height')
    height_unit = fields.Selection('_units', string='Unit Measure', default="mm")

    # font
    font_size = fields.Float(string="Font Size", default=4)
    font_unit = fields.Selection('_units', string='Unit Measure', default="mm")
    font_bold = fields.Boolean(string='Bold')
    font_italic = fields.Boolean(string='Italic')
    text_align = fields.Selection(
        [
            ('center', 'Center'),
            ('justify', 'Justify'),
            ('left', 'Left'),
            ('right', 'Right'),
        ],
        string='Text Align',
    )
    font_color = fields.Selection(COLOR_LIST, string='Font Color',)

    border_top = fields.Boolean(string='Border Top',)
    border_bottom = fields.Boolean(string='Border Bottom',)
    border_left = fields.Boolean(string='Border Left',)
    border_right = fields.Boolean(string='Border Right',)

    border_top_size = fields.Float(string='B.Top Size', default=1)
    border_bottom_size = fields.Float(string='B.Bottom Size', default=1)
    border_left_size = fields.Float(string='B.Left Size', default=1)
    border_right_size = fields.Float(string='B.Right Size', default=1)

    border_top_unit = fields.Selection('_units', string='Border Top Unit', default='px')
    border_bottom_unit = fields.Selection('_units', string='Border Bottom Unit', default='px')
    border_left_unit = fields.Selection('_units', string='Border Left Unit', default='px')
    border_right_unit = fields.Selection('_units', string='Border Right Unit', default='px')

    border_top_style = fields.Selection('_border_styles', string='Border Top Style', default='solid')
    border_bottom_style = fields.Selection('_border_styles', string='Border Bottom Style', default='solid')
    border_left_style = fields.Selection('_border_styles', string='Border Left Style', default='solid')
    border_right_style = fields.Selection('_border_styles', string='Border Right Style', default='solid')

    border_top_color = fields.Selection(COLOR_LIST, string='Border Top',)
    border_bottom_color = fields.Selection(COLOR_LIST, string='Border Bottom',)
    border_left_color = fields.Selection(COLOR_LIST, string='Border Left',)
    border_right_color = fields.Selection(COLOR_LIST, string='Border Right',)

    prefix = fields.Char(
        string='Prefix',
        help='This text will appear on the left side of the printed value'
    )
    suffix = fields.Char(
        string='Suffix',
        help='This text will appear on the right side of the printed value'
    )
    sample = fields.Char(string='Sample', compute='_compute_sample')

    @api.depends('prefix', 'suffix')
    def _compute_sample(self):
        for rec in self:
            pr = rec.prefix or ''
            su = rec.suffix or ''

            rec.sample = "%sThis is a Sample%s" % (pr, su)

    @api.onchange('is_matrix')
    def _onchange_is_matrix(self):
        if self.is_matrix:
            self.height_f = True
            self.height = 5.0

    @api.onchange('from_model')
    def _onchange_from_model(self):
        pass

    @api.onchange('from_model_id')
    def _onchange_from_model_id(self):
        self._check_from_model_id()
        if self.from_model_id:
            self.from_model = self.from_model_id.model_name
            self.is_matrix = self.from_model_id.is_matrix
            self.matrix_field = self.from_model_id.matrix_field or ''

    @api.one
    @api.constrains('from_model_id')
    def _check_from_model_id(self):
        if self.from_model_id and self.from_model_id.main_model_id.id != self.format_id.main_model_id.id:
            tstr = "In Line '%s'" % (self.name or self.other_field)
            raise ValidationError(_("The Model '%s' is not allowed in this format. %s") % (self.from_model_id.name, tstr))

    def _arguments(self):
        arguments_l = [
            ('other_field', 'Field'),
            ('frame', 'Frame'),
            ('image', 'Image'),
            ('text', 'Text'),
            ('copy', 'Copy Title'),
        ]
        return arguments_l

    def _arguments_type(self):
        arguments_type_l = [
            ('text', 'Text / General'),
            ('date', 'Date'),
            ('number', 'Number'),
            ('currency', 'Currency'),
            ('image', 'Image'),
        ]
        return arguments_type_l

    def _format_number(self):
        arguments_number_l = [
            ('number', 'General'),
            ('to_text', 'Convert To Text'),
        ]
        return arguments_number_l

    def _units(self):
        unit_l = [
            ('mm', 'mm'),
            ('cm', 'cm'),
            ('in', 'in'),
            ('px', 'Pixels'),
            ('pt', 'Points'),
        ]
        return unit_l

    def _border_styles(self):
        unit_l = [
            ('dotted', 'dotted border'),
            ('dashed', 'dashed border'),
            ('solid', 'solid border'),
            ('double', 'double border'),
            ('groove', '3D grooved border'),
            ('ridge', '3D ridged border'),
            ('inset', '3D inset border'),
            ('outset', '3D outset border'),
            ('none', 'Defines no border'),
            ('hidden', 'Defines a hidden border'),
        ]
        return unit_l


class WizardFormatPrint(models.TransientModel):
    _name = 'wizard.formats.print'

    format_id = fields.Many2one('format.print', string="Format Print")

    @api.multi
    def action_call_report(self):
        data = self.read()[0]
        if self.format_id.paper_format_id and self.format_id.page_height <= 0 or self.format_id.page_width <= 0:
            raise Warning(_("Page height and width can not be less than Zero(0)."))
        result = self.format_id.paper_format_id.write({
            'format': 'custom',
            'page_width': self.format_id.page_width,
            'page_height': self.format_id.page_height,
        })
        datas = {
            'ids': self._context.get('active_id'),
            'model': 'wizard.formats.print',
            'form': data
        }
        return self.env['report'].get_action(self, 'vitt_format_print.format_print_template', data=datas)


class FormatPrintMainModels(models.Model):
    _name = 'format.print.main_models'

    model_name = fields.Char(string='Model')
    name = fields.Char(string='Name', translate=True)
    child_models_ids = fields.One2many('format.print.child_models', 'main_model_id', string='Child Models')


class FormatPrintChildModels(models.Model):
    _name = 'format.print.child_models'

    main_model_id = fields.Many2one('format.print.child_models', string='Main Model', ondelete='cascade')
    model_name = fields.Char(string='Model')
    name = fields.Char(string='Name', translate=True)
    is_matrix = fields.Boolean(string='Is Matrix')
    matrix_field = fields.Char(string='Matrix Field')
