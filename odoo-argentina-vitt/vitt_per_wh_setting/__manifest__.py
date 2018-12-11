# -*- coding: utf-8 -*-
{
    'name': 'Seteo de provincias para percepciones y retenciones',
    'summary': 'Seteo de provincias para percepciones y retenciones',
    'description': """Seteo de provincias para percepciones y retenciones""",
    'version': '10.0.1.0',
    'author': 'Moogah',
    'website': 'http://www.moogah.com',
    'depends': [
        'l10n_ar_account_withholding',
        'vitt_sales_reports',
    ],
    'data': [
        'views/res_config.xml',
        'views/res_country_state.xml',
    ],
    'installable': True,
}
