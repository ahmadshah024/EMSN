# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassRoom(models.Model):
    _inherit = 'ems.student'


    discount_id = fields.Many2one('ems.finance.discount')

    # finance_ids = fields.One2many('ems.finance', 'student_id')


    def action_open_finance(self):
        for rec in self:
            return {
                'name': 'finances for Student',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.finance',
                'view_mode': 'tree,form',
                'domain': [('student_id', '=', rec.id)],
            }