# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, models, tools, _
from odoo.exceptions import Warning
from odoo.tools.misc import formatLang
import datetime
import locale


class FormatPrintTemplate(models.AbstractModel):
    _name = 'report.vitt_format_print.format_print_template'

    @api.multi
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('vitt_format_print.format_print_template')
        form = data.get('form')
        format_id = form.get('format_id')
        if format_id:
            format_print = self.env['format.print'].browse([format_id[0]])
            records = self.env[format_print.main_model].browse(data["ids"])

        arguments_lines = self._get_arguments_lines(data['form'])
        copies_lines = self._get_copies_lines(data['form'])

        docargs = {
            'doc_ids': records,
            'doc_model': report.model,
            'docs': self,
            'arguments_lines': arguments_lines,
            'copies_lines': copies_lines,
            'get_style': self._get_style,
            'get_value': self._get_value,
            'data': data
        }
        return report_obj.render('vitt_format_print.format_print_template', docargs,)

    def _get_arguments_lines(self, data):
        format_id = data.get('format_id')
        if format_id:
            format_print = self.env['format.print'].browse([format_id[0]])
            if format_print and format_print.arguments_line_ids:
                return format_print.arguments_line_ids

    def _get_copies_lines(self, data):
        format_id = data.get('format_id')
        if format_id:
            format_print = self.env['format.print'].browse([format_id[0]])
            if format_print and format_print.copies_line_ids:
                return format_print.copies_line_ids

    def _get_style(self, data, arg_id=None, line_pos=1.0):
        # position = style = font = top = left = width = height = bold = italic = text_align = font_color = ""
        position = style = ""

        if arg_id:
            arg_line = self.env['format.arguments.lines'].browse([int(arg_id)])

        position = 'position:absolute;'
        style += position
        if arg_line:
            if arg_line.is_matrix:
                row_height = (arg_line.height) * line_pos
            else:
                row_height = 0.0
            if arg_line.font_size:
                style += 'font-size: %s;' % (str(arg_line.font_size) + arg_line.font_unit)
            if arg_line.top_margin:
                style += 'top: %s;' % (str(arg_line.top_margin + row_height) + arg_line.top_unit)
            if arg_line.left_margin:
                style += 'left: %s;' % (str(arg_line.left_margin) + arg_line.left_unit)
            if arg_line.width:
                style += 'width: %s;' % (str(arg_line.width) + arg_line.width_unit)
                if arg_line.arguments == 'image':
                    style += 'max-width: %s;' % (str(arg_line.width) + arg_line.width_unit)
            if arg_line.height:
                style += 'height: %s;' % (str(arg_line.height) + arg_line.height_unit)
                if arg_line.arguments == 'image':
                    style += 'max-height: %s;' % (str(arg_line.height) + arg_line.height_unit)
            if arg_line.font_bold:
                style += 'font-weight: bold;'
            if arg_line.font_italic:
                style += 'font-style: italic;'
            if arg_line.text_align:
                style += 'text-align: %s;' % arg_line.text_align
            if arg_line.font_color:
                style += 'color: %s;' % arg_line.font_color

            # borders
            if arg_line.border_top:
                border_style = arg_line.border_top_style or ""
                border_color = arg_line.border_top_color or ""
                style += 'border-top: %s %s %s;' % ((str(arg_line.border_top_size) + arg_line.border_top_unit), border_style, border_color)
            if arg_line.border_bottom:
                border_style = arg_line.border_bottom_style or ""
                border_color = arg_line.border_bottom_color or ""
                style += 'border-bottom: %s %s %s;' % ((str(arg_line.border_bottom_size) + arg_line.border_bottom_unit), border_style, border_color)
            if arg_line.border_left:
                border_style = arg_line.border_left_style or ""
                border_color = arg_line.border_left_color or ""
                style += 'border-left: %s %s %s;' % ((str(arg_line.border_left_size) + arg_line.border_left_unit), border_style, border_color)
            if arg_line.border_right:
                border_style = arg_line.border_right_style or ""
                border_color = arg_line.border_right_color or ""
                style += 'border-right: %s %s %s;' % ((str(arg_line.border_right_size) + arg_line.border_right_unit), border_style, border_color)

            # style = '%s %s %s %s %s %s %s %s %s %s' % (position, font, top, left, width, height, bold, italic, text_align, font_color)

        return style

    def _get_value(self, data, record_id=None, arg_id=None):

        res = value_field = ""
        arg_line = record = None

        if arg_id:
            arg_line = self.env['format.arguments.lines'].browse([int(arg_id)])
        else:
            return

        if record_id:
            record = self.env[arg_line.from_model].browse([int(record_id)])

        if not arg_line or not record:
            return res

        argument = arg_line.arguments

        # make other field
        _field = arg_line.other_field or arg_line.image_field
        if argument in ["other_field", "image"] and _field:
            value_field = self._get_value_from_object(_field, record)

            if value_field and arg_line.argument_type == 'date':
                try:
                    lang_code = self.env.user.lang or 'en_US'
                    locale.setlocale(locale.LC_ALL, str(lang_code))
                except:
                    pass

                dt = value_field
                format_date = arg_line.format_date or '%Y-%m-%d'
                value_field = datetime.datetime.strptime(dt, '%Y-%m-%d').strftime(format_date)  # this return Day, Month or Year in a specific format

            # Number Format
            if value_field and arg_line.argument_type in ['number', 'currency']:
                value = value_field
                if value:
                    value_field = self._get_format_number(record, arg_line, value) or ""

        if argument == "text" and arg_line.other_text:
            value_field = arg_line.other_text

        res = value_field or ""
        prf = arg_line.prefix or ""
        suf = arg_line.suffix or ""

        try:
            u''.join(res).encode('utf-8')
        except:
            str(res)

        res = prf + res + suf
        return res

    def _get_value_from_object(self, other_field=None, record=None):
        arg_list = other_field.split(".")  # convert list the "other_field" to get object by object
        obj_temp = record
        for arg in arg_list:  # get object by object
            if not hasattr(obj_temp, arg):
                return ""

            obj_temp = getattr(obj_temp, arg)

        if obj_temp:
            try:
                u''.join(obj_temp).encode('utf-8')
                return obj_temp
            except:
                return str(obj_temp)

    def _get_format_number(self, record=None, arg_line=None, value=None):
        try:
            nr = float(value)
        except:
            nr = 0.0

        currency_name = ''
        currency_id = currency_obj = None
        val2words_default = arg_line.format_id.company_id.val2words_default
        if arg_line.argument_type == 'currency':
            if hasattr(record, 'currency_id'):
                currency_id = record.currency_id.id
            else:
                currency_id = self.company_id.currency_id.id

            if currency_id:
                currency_obj = self.env['res.currency'].browse([currency_id])
                domain = [
                    ('config_id', '=', val2words_default.id),
                    ('currency_id', '=', currency_id),
                ]
                currency_names_obj = self.env['vitt_val2words.currency_names'].search(domain)

                try:
                    currency_name = currency_names_obj.currency_name or currency_obj.name
                except:
                    currency_name = ''

        if arg_line.format_number == 'to_text':
            res = val2words_default._num_to_text(num=nr, currency=currency_name) or ''
        else:
            tstr = formatLang(self.env, nr, currency_obj=currency_obj),
            res = tstr[0]

        return res or ""
