# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError



class EmsLibrary(models.Model):
    _name = 'ems.library'
    _description = 'ems_library'

    name = fields.Char(readonly=True, default="New", states={'done': [('readonly', True)]})
    date = fields.Date(string='Date', default=lambda self: fields.Date.today(), states={'done': [('readonly', True)]})
    days = fields.Integer(string='Days', states={'done': [('readonly', True)]},required=True)
    return_date = fields.Date(string='Return Date', compute='_compute_return_date', store=True, states={'done': [('readonly', True)]})
    student_id = fields.Many2one('ems.student', states={'done': [('readonly', True)]}, required=True)
    library_line_ids = fields.One2many('ems.library.line', 'library_id', states={'done': [('readonly', True)]})
    is_returned = fields.Boolean(default=False, states={'done': [('readonly', True)]})
    state = fields.Selection([
    ('draft', 'Draft'),
    ('waiting', 'Waiting'),  # Add the 'Waiting' state
    ('done', 'Done'),
    ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'done': [('readonly', True)]})

    def action_mark_done(self):
        for record in self:
            if not record.is_returned:
                raise ValidationError('the book has not returned yet')
            record.state = 'done'

    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'

    def action_mark_waiting(self):
        for record in self:
            for library_line in record.library_line_ids:
                book = library_line.book_id
                if book.available <= 0:
                    raise ValidationError('Book is not available')
                if book.copy_amount <= 0:
                    raise ValidationError('No more copies available')
                book.write({'state': 'assigned', 'available': book.available - 1, 'copy_amount': book.copy_amount - 1})
            record.state = 'waiting'
    # def action_mark_waiting(self):
    #     for record in self:
    #         record.library_line_ids.book_id.state= 'assigned'
    #         record.library_line_ids.book_id.available = record.library_line_ids.book_id.copy_amount - 1
    #         if record.library_line_ids.book_id.available < 1:
    #             raise ValidationError('Book is not available') 
    #         record.state = 'waiting'



    @api.depends('date', 'days')
    def _compute_return_date(self):
        for request in self:
            if request.date and request.days:
                return_date = request.date + timedelta(days=request.days)
                request.return_date = return_date
            else:
                request.return_date = False




    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('ems.library.sequence')
        return super(EmsLibrary, self).create(vals)
    
    



class EmsLibraryLine(models.Model):
    _name = 'ems.library.line'
    _description = 'ems_library'

    library_id = fields.Many2one('ems.library')
    
    book_id = fields.Many2one('ems.library.books') 
    author = fields.Char(related='book_id.author')
    language = fields.Char(related='book_id.language')
    subjects = fields.Char( related='book_id.subjects')



    # @api.depends('book_id')
    # def _onchange_book_id(self):
    #     for rec in self:
    #         borrowed_copies = self.env['    '].search_count([('book_id', '=', rec.book_id.id)])
    #         if rec.book_id.copy_amount <= borrowed_copies:
    #             raise ValidationError('All copies of this book have been borrowed. Cannot borrow more.')




class EmsBook(models.Model):
    _name = 'ems.library.books'
    _description = 'ems.library.book'

    name = fields.Char()
    author = fields.Char()
    pages = fields.Char()
    subjects = fields.Char()
    title = fields.Char(string='Title', required=True)
    language = fields.Char(string='Language')
    cover_image = fields.Binary(string='Cover Image')
    publication_date = fields.Date(string='Publication Date')
    description = fields.Text(string='Description')
    copy_amount = fields.Integer(string='Copy Amount')
    available = fields.Integer(string='Available Amount', readonly=True)
    state = fields.Selection([
        ('free', 'Free'),
        ('assigned', 'Assigned'),
    ], string='State', default='free')


    
  





    

