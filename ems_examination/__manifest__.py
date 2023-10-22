# -*- coding: utf-8 -*-
{
    'name': "ems_examination",

    'summary': """
       ems_examination""",

    'description': """
       ems_examination
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'ems-student', 'ems_timetable', 'ems_teacher'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ems_examination_views.xml',
        'views/ems_examination_result_views.xml',
        'data/sequence.xml',
    ],
}
