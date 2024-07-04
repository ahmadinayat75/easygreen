# # -*- coding: utf-8 -*-
# from odoo import http
# from odoo.http import request
# import itertools
#
# class Export(http.Controller):
#
#     @http.route('/web/export/namelist', type='json', auth="user")
#     def namelist(self, model, export_id):
#         # TODO: namelist really has no reason to be in Python (although itertools.groupby helps)
#         print('OKAY')
#         print('export_id', export_id)
#         export = request.env['ir.exports'].browse([export_id]).read()[0]
#         export_fields_list = request.env['ir.exports.line'].browse(export['export_fields']).read()
#
#         fields_data = self.fields_info(
#             model, [f['name'] for f in export_fields_list])
#
#         return [
#             {'name': field['name'], 'label': fields_data[field['name']]}
#             for field in export_fields_list
#         ]
#     def fields_info(self, model, export_fields):
#         info = {}
#         fields = self.fields_get(model)
#         if ".id" in export_fields:
#             fields['.id'] = fields.get('id', {'string': 'ID'})
#
#         # To make fields retrieval more efficient, fetch all sub-fields of a
#         # given field at the same time. Because the order in the export list is
#         # arbitrary, this requires ordering all sub-fields of a given field
#         # together so they can be fetched at the same time
#         #
#         # Works the following way:
#         # * sort the list of fields to export, the default sorting order will
#         #   put the field itself (if present, for xmlid) and all of its
#         #   sub-fields right after it
#         # * then, group on: the first field of the path (which is the same for
#         #   a field and for its subfields and the length of splitting on the
#         #   first '/', which basically means grouping the field on one side and
#         #   all of the subfields on the other. This way, we have the field (for
#         #   the xmlid) with length 1, and all of the subfields with the same
#         #   base but a length "flag" of 2
#         # * if we have a normal field (length 1), just add it to the info
#         #   mapping (with its string) as-is
#         # * otherwise, recursively call fields_info via graft_subfields.
#         #   all graft_subfields does is take the result of fields_info (on the
#         #   field's model) and prepend the current base (current field), which
#         #   rebuilds the whole sub-tree for the field
#         #
#         # result: because we're not fetching the fields_get for half the
#         # database models, fetching a namelist with a dozen fields (including
#         # relational data) falls from ~6s to ~300ms (on the leads model).
#         # export lists with no sub-fields (e.g. import_compatible lists with
#         # no o2m) are even more efficient (from the same 6s to ~170ms, as
#         # there's a single fields_get to execute)
#         for (base, length), subfields in itertools.groupby(
#                 sorted(export_fields),
#                 lambda field: (field.split('/', 1)[0], len(field.split('/', 1)))):
#             subfields = list(subfields)
#             if length == 2:
#                 # subfields is a seq of $base/*rest, and not loaded yet
#                 info.update(self.graft_subfields(
#                     fields[base]['relation'], base, fields[base]['string'],
#                     subfields
#                 ))
#             elif base in fields:
#                 info[base] = fields[base]['string']
#
#         return info
# # class DynamicStrings(http.Controller):
# #     @http.route('/dynamic_strings/dynamic_strings', auth='public')
# #     def index(self, **kw):
# #         return "Hello, world"
#
# #     @http.route('/dynamic_strings/dynamic_strings/objects', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('dynamic_strings.listing', {
# #             'root': '/dynamic_strings/dynamic_strings',
# #             'objects': http.request.env['dynamic_strings.dynamic_strings'].search([]),
# #         })
#
# #     @http.route('/dynamic_strings/dynamic_strings/objects/<model("dynamic_strings.dynamic_strings"):obj>', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('dynamic_strings.object', {
# #             'object': obj
# #         })
