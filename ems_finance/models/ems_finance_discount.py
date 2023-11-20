# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EmsFinanceDiscount(models.Model):
    _name = 'ems.finance.discount'
    _description = 'ems finance discount description'

    name = fields.Char()
    discount_amount = fields.Integer()
    reason = fields.Text()

    student_ids = fields.One2many('ems.student', 'discount_id')
    def action_open_students(self):
        students_with_discount = self.mapped('student_ids')  # Assuming student_ids is the Many2many field linking students to discounts
        return {
            'name': 'Students',
            'type': 'ir.actions.act_window',
            'res_model': 'ems.student',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', students_with_discount.ids)],
        }