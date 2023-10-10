# -*- coding: utf-8 -*-

from odoo import models, fields


class ClassRoom(models.Model):
    _inherit = 'ems.class.room'

    curriculum_line_ids = fields.One2many('ems.curriculum.line','class_id')
    curriculum_line_count = fields.Integer(compute='_compute_books_count')

    def _compute_books_count(self):
        for book in self:
            book.curriculum_line_count = len(book.curriculum_line_ids)

    def action_open_books(self):
        for rec in self:
            book_ids = rec.curriculum_line_ids.mapped('book_id')
            return {
                'name': 'Books',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.book',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', book_ids.ids)],
            }
        
