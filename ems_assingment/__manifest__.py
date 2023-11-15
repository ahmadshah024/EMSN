# -*- coding: utf-8 -*-
{
    'name': "ems_assingment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','ems-student','ems_timetable'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_schedule.xml',
        'data/mail_activity_date.xml',
        'views/ems_assignment_view.xml',
        'views/ems_student_view.xml',
        'views/ems_teacher_view.xml',
        'views/ems_class_room_view.xml',
        'wizards/submit_assignment_wizard.xml',

    ],
    
}
