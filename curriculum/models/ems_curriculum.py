# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsCurriculum(models.Model):
    _name = 'ems.curriculum'
    _description = 'curriculum'

    name = fields.Char(required=True)
    reference = fields.Char(readonly=True)
    book_ids = fields.One2many("ems.book", "curriculum_id")
    

 
    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.curriculum.sequence')
        return super(EmsCurriculum, self).create(vals)
    

class EmsBook(models.Model):
    _name = 'ems.book'
    _description = 'book'

    name = fields.Char(required=True)
    publication_date = fields.Date(string='Publication Date')
    author = fields.Char()
    pages = fields.Integer()
    curriculum_id = fields.Many2one("ems.curriculum")