# -*- coding: utf-8 -*-
{
    'name': "curriculum",

    'summary': """
       curriculum""",

    'description': """
       curriculum
    """,

    'author': "Netlinks",
    'website': "https://www.netlinks.ltd.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','ems-student'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ems_curriculum_views.xml',
        'views/ems_books_views.xml',
        'data/sequence.xml',

  
    ],

}
