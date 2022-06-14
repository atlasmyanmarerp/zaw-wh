# -*- coding: utf-8 -*-
# from odoo import http


# class NpCustom(http.Controller):
#     @http.route('/np_custom/np_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/np_custom/np_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('np_custom.listing', {
#             'root': '/np_custom/np_custom',
#             'objects': http.request.env['np_custom.np_custom'].search([]),
#         })

#     @http.route('/np_custom/np_custom/objects/<model("np_custom.np_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('np_custom.object', {
#             'object': obj
#         })
