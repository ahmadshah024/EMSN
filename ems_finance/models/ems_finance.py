# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsFinance(models.Model):
    _name = 'ems.finance'
    _description = 'ems finance description'

    name = fields.Char(readonly=True, default='New')
    student_id = fields.Many2one('ems.student')
    student_class = fields.Many2one(related='student_id.class_id')
    date = fields.Date(default=fields.Date.today())
    is_enrollment = fields.Boolean(default=False)
    is_monthly_fee = fields.Boolean(default=False)
    is_uniform_fee = fields.Boolean(default=False)
    is_book = fields.Boolean(default=False)
    finance_line_ids = fields.One2many('ems.finance.enrollment.line', 'finance_id')
    finance_month_line_ids = fields.One2many('ems.finance.month.line', 'finance_id')
    finance_uniform_line_ids = fields.One2many('ems.finance.uniform.line', 'finance_id')
    finance_book_line_ids = fields.One2many('ems.finance.book.line', 'finance_id')
    
    
    

    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('ems.finance.sequence')
        return super(EmsFinance, self).create(vals)
    

class EmsFinanceEnrollmentLine(models.Model):
    _name = 'ems.finance.enrollment.line'
    _description = 'ems finance description'


    # uniform_id = fields.Many2one('product_template', domain=[('is_uniform', '=', True)])
    # uniform_price = fields.Integer(related='uniform_id.')
    # book_id = fields.Many2one('product_template', domain=[('is_uniform', '=', True)])
    registration_fee = fields.Integer()
    monthly_fee = fields.Integer()
    uniform_fee = fields.Integer()
    books_fee = fields.Integer()
    total = fields.Integer(compute="_compute_enrollment_total")
    finance_id = fields.Many2one('ems.finance')


    @api.depends('registration_fee', 'monthly_fee', 'uniform_fee', 'books_fee')
    def _compute_enrollment_total(self):
        for rec in self:
            rec.total = rec.registration_fee + rec.monthly_fee + rec.uniform_fee + rec.books_fee


class EmsFinanceMonthLine(models.Model):
    _name = 'ems.finance.month.line'
    _description = 'ems finance month description'


    monthly_fee = fields.Integer()
    month = fields.Char()
    number_of_month = fields.Integer()
    total = fields.Integer(compute="_compute_month_total")
    finance_id = fields.Many2one('ems.finance')

    @api.depends('monthly_fee','number_of_month')
    def _compute_month_total(self):
        for rec in self:
            rec.total = rec.monthly_fee * rec.number_of_month


class EmsFinanceUniformLine(models.Model):
    _name = 'ems.finance.uniform.line'
    _description = 'ems finance uniform description'


    uniform_id = fields.Many2one('product.template', domain=[('is_uniform', '=', True)])
    # uniform_price = fields.Integer(related='uniform_id.price')
    pices = fields.Integer()
    total = fields.Integer()
    finance_id = fields.Many2one('ems.finance')


    @api.depends('uniform_price', 'pices')
    def _compute_uniform_total(self):
        for rec in self:
            rec.total = rec.uniform_price * rec.pices




class EmsFinanceBookLine(models.Model):
    _name = 'ems.finance.book.line'
    _description = 'ems finance book description'


    book_id = fields.Many2one('product.template', domain=[('is_book', '=', True)])
    total = fields.Integer()
    finance_id = fields.Many2one('ems.finance')


    # @api.depends('registration_fee', 'monthly_fee', 'uniform_fee', 'books_fee')
    # def _compute_enrollment_total(self):
    #     for rec in self:
    #         rec.total = rec.registration_fee + rec.monthly_fee + rec.uniform_fee + rec.books_fee


# class EmsStockUniform(models.Model):
#     _name = 'ems.stock.uniform'
#     _description = 'ems stock uniform description'

#     name = fields.Char()
#     uniform_type = fields.Selection(
#         [
#         ('shirt', 'Shirt or Blouse'),
#         ('pants', 'Pants'),
#         ('skirt', 'Skirt'),
#         ('tie', 'Tie or Necktie'),
#         ('jacket', 'Jacket or Blazer'),
#         ('full', 'Full'),
#         ]
#     )

#     all_suite_price = fields.Integer('Suite price')
#     shirt_price = fields.Integer('Shirt price')
#     pants_price = fields.Integer('Pants price')
#     skirt_price = fields.Integer('Skirt price')
#     tie_price = fields.Integer('Tie price')
#     jacket_price = fields.Integer('Jacket price')

#     price = fields.Integer('Price')


#     all_suite_onhand = fields.Integer('Suite Onhand')
#     shirt_onhand = fields.Integer('Shirt Onhand')
#     pants_onhand = fields.Integer('Pants Onhand')
#     skirt_onhand = fields.Integer('Skirt Onhand')
#     tie_onhand = fields.Integer('Tie Onhand')
#     jacket_onhand = fields.Integer('Jacket Onhand')
    


#     @api.depends('price')
#     def _compute_price(self):
#         for rec in self:
#             if rec.uniform_type == 'full':
#                 rec.all_suite_price = rec.price
#             elif rec.uniform_type == 'full':
#                 rec.all_suite_price = rec.price

             



# class EmsStockBook(models.Model):
#     _name = 'ems.stock.book'
#     _description = 'ems stock book description'

#     name = fields.Char()
#     class_name = fields.Char()
#     book_type = fields.Selection(
#         [
#         ('private', 'Private'),
#         ('governmental', 'Governmental'),
#         ]
#     )

#     private_price = fields.Integer(compute="_compute_price")
#     governmental_price = fields.Integer(compute="_compute_price")
#     price = fields.Integer()


#     @api.depends('price')
#     def _compute_price(self):
#         for rec in self:
#             if rec.book_type == 'private':
#                 rec.private_price = rec.price
#             else:
#                 rec.governmental_price = rec.price

    
#     # @api.depends('price')
#     # def compute_governmental_price(self):
#     #     for rec in self:
#     #         if rec.book_type == 'governmental':
                