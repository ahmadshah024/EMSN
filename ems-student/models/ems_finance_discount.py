# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsFinanceDiscount(models.Model):
    _inherit = 'ems.finance.discount'


    
    def action_open_students(self):
        for rec in self:
            return {
                'name': 'Students',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.student',
                'view_mode': 'tree,form',
                # 'domain': [('student_id', '=', rec.id)],
                # 'context': {
                # 'default_student_id': rec.id,  # Pass the student's ID as the default value
                # 'search_default_student_id': rec.student_id.id,  # Set the search default
            }
            