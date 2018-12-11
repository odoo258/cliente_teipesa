# -*- coding: utf-8 -*-
from odoo import http

# class TeipesaResPartner(http.Controller):
#     @http.route('/teipesa_res_partner/teipesa_res_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/teipesa_res_partner/teipesa_res_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('teipesa_res_partner.listing', {
#             'root': '/teipesa_res_partner/teipesa_res_partner',
#             'objects': http.request.env['teipesa_res_partner.teipesa_res_partner'].search([]),
#         })

#     @http.route('/teipesa_res_partner/teipesa_res_partner/objects/<model("teipesa_res_partner.teipesa_res_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('teipesa_res_partner.object', {
#             'object': obj
#         })