# -*- coding: utf-8 -*-
{
    'name': "sale_timesheet_extend",

    'summary': """
        This Module will Replace the sale_timesheet module functionality and show the project Income/expense From JV or JE """,

    'description': """
        This Module will Replace the sale_timesheet module functionality and show the project Income/expense From JV or JE
    """,

    'author': "Ahmad Inayat +923349275408",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_timesheet','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
