# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsCurriculum(models.Model):
    _name = 'ems.curriculum'
    _description = 'curriculum'


    name = fields.Char(string='Curriculum Name', required=True)
    # book_name = fields.Char(string='Book Names', related='book_ids.name', store=True)
    reference = fields.Char(readonly=True, default="New")
    class_id = fields.Many2one('ems.class.room')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'done': [('readonly', True)]})
    acadomic_year = fields.Date()
    curriculum_line_ids = fields.One2many('ems.curriculum.line', 'curriculum_id')


 
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
    

class EmsCurriculumLine(models.Model):
    _name = 'ems.curriculum.line'
    _description = 'ems curvericulum line'


    book_id = fields.Many2one('ems.book')
    author = fields.Char(related='book_id.author')
    page = fields.Integer(related='book_id.pages')


    curriculum_id = fields.Many2one('ems.curriculum')




class EmsBook(models.Model):
    _name = 'ems.book'
    _description = 'book'


    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'done': [('readonly', True)]})
    
    name = fields.Char(string='Book Name', required=True)
    publication_date = fields.Date(string='Publication Date')
    author = fields.Char()
    pages = fields.Integer()
    image = fields.Binary()


    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    
    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'   
    
