# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsCurriculum(models.Model):
    _name = 'ems.curriculum'
    _description = 'curriculum'


    name = fields.Char(string='Curriculum Name', required=True)
    book_ids = fields.One2many('ems.book', 'curriculum_id', string='Books')
    book_name = fields.Char(string='Book Names', related='book_ids.name', store=True)
    reference = fields.Char(readonly=True, default="New")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'done': [('readonly', True)]})
    acadomic_year = fields.Date()
    

 
    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    
    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'   
    

 
    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.curriculum.sequence')
        return super(EmsCurriculum, self).create(vals)
    

class EmsBook(models.Model):
    _name = 'ems.book'
    _description = 'book'

    
    name = fields.Char(string='Book Name', required=True)
    publication_date = fields.Date(string='Publication Date')
    author = fields.Char()
    pages = fields.Integer()
    curriculum_id = fields.Many2one('ems.curriculum', string='Curriculum')