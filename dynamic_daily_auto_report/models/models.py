# -*- coding: utf-8 -*-

from odoo import models, fields, api
import io
import xlsxwriter
from odoo.tools import pycompat
import base64
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes


class DailyReportLogs(models.Model):
    _name = 'daily.report.logs'
    _description = 'Dynamic Excel Report Templates'

    name = fields.Char()
    date = fields.Date()
    status = fields.Char()
    customer_id = fields.Many2one('res.partner')
    email = fields.Char()


class DynamicExcelReport(models.Model):
    _name = 'dynamic.excel.report'
    _description = 'Dynamic Excel Report Templates'

    name = fields.Char()
    customer = fields.Many2one('res.partner')
    template = fields.Many2one('ir.exports')
    to = fields.Char()
    status = fields.Selection([('draft', 'Draft'), ('running', 'Running')])

    def attach_excel_to_email(self, id):
        headers = []
        header_strings = []
        temp = self.browse(id)
        template = temp.template
        template_id = self.env['ir.exports.line'].search([('export_id', '=', template.id)])
        for rec in template_id:
            headers.append(rec.name)
            strings = self.env['ir.model.fields'].search([('model', '=', template.resource),
                                                          ('name', '=', rec.name)], limit=1).field_description
            header_strings.append(strings)
        data = self.env[template.resource].sudo().search_read(domain=[('customer_id', '=', temp.customer.id),
                                                   ('total_quantity', '>', 0), ('active', '=', True)], fields=headers)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:Z', 16)
        for col, header in enumerate(header_strings):
            worksheet.write(0, col, header)
        for row, record in enumerate(data, start=1):
            for col, header in enumerate(headers):
                for rows, rec in record.items():
                    if isinstance(rec, (list, tuple)):
                        record[rows] = rec[1]
                    if isinstance(rec, bool):
                        record[rows] = ''
                worksheet.write(row, col, record.get(header, ''))
        workbook.close()
        return output.getvalue()

    def get_excel_report(self):
        template_ids = self.search([('status', '=', 'running')])
        if template_ids:
            for rec in template_ids:
                attachment_data = self.attach_excel_to_email(rec.id)
                file_name = 'SOH_' + rec.customer.name + '_' + str(fields.Date.today().strftime('%d-%m-%Y')) + '.xlsx'
                attachment = self.env['ir.attachment'].create({
                    'name': file_name,
                    'type': 'binary',
                    'datas': base64.b64encode(attachment_data),
                    'store_fname': file_name,
                    'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                })
                template = self.env.ref('dynamic_daily_auto_report.mail_template_dynamic_stock_on_hand_report')
                if template:
                    template.email_to = rec.to
                    template.attachment_ids = [(6, 0, [attachment.id])]
                    template.send_mail(rec.id, force_send=True)
                    self.env['daily.report.logs'].create({'name': file_name, 'date': fields.Datetime.now(),'email': rec.to,
                                                          'status': 'Success', 'customer_id': rec.customer.id})


class IrExports(models.Model):
    _inherit = 'ir.exports'
    _description = 'Extend Excel Report Templates'

    @api.model
    def get_user_list(self, model):
        vals = []
        list = self.search([('resource', '=', model), ('resource', '=', model)])
        customer_ids = self.env['res.users'].sudo().browse(list.create_uid.ids).customer_ids.ids
        allowed_customer = self.env['res.users'].sudo().browse(self.env.uid).customer_ids.ids
        result = [i for i in customer_ids if i in allowed_customer]
        user_list = self.env['res.users'].search([('customer_ids', 'in', result)]).ids
        lists = self.env['ir.exports'].search([('resource', '=', model), ('create_uid', 'in', user_list)])
        for rec in lists:
            vals.append({'id': rec.id, 'name': rec.name})
        return vals




