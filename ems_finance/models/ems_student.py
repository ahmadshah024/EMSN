# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassRoom(models.Model):
    _inherit = 'ems.student'


    discount_id = fields.Many2one('ems.finance.discount')

    finance_id = fields.Many2one('ems.finance')
    # finance_count = fields.Integer(compute='_compute_finance_count', string='finance Count')


    # @api.depends('finance_id')
    # def _compute_finance_count(self):
    #     for rec in self:
    #         rec.finance_count = rec.env['ems.finance.line'].search_count([
    #             ('student_id', '=', rec.id),
    #         ])
 


    def action_open_finance(self):
        for rec in self:
            return {
                'name': 'finances for Student',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.finance',
                'view_mode': 'tree,form',
                'domain': [('student_id', '=', rec.id)],
            }