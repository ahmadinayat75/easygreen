# -*- coding: utf-8 -*-
# from odoo import http


# class SaleTimesheetExtend(http.Controller):
#     @http.route('/sale_timesheet_extend/sale_timesheet_extend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_timesheet_extend/sale_timesheet_extend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_timesheet_extend.listing', {
#             'root': '/sale_timesheet_extend/sale_timesheet_extend',
#             'objects': http.request.env['sale_timesheet_extend.sale_timesheet_extend'].search([]),
#         })

#     @http.route('/sale_timesheet_extend/sale_timesheet_extend/objects/<model("sale_timesheet_extend.sale_timesheet_extend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_timesheet_extend.object', {
#             'object': obj
#         })
