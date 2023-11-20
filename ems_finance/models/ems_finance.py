# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class EmsFinance(models.Model):
    _name = 'ems.finance'
    _description = 'ems finance description'

    name = fields.Char(readonly=True, default='New')
    student_id = fields.Many2one('ems.student', states={'approved': [('readonly', True)]})
    student_class = fields.Many2one(related='student_id.class_id', states={'approved': [('readonly', True)]})
    date = fields.Date(default=fields.Date.today(), states={'approved': [('readonly', True)]})
    invoice_type = fields.Selection(
        [
            ('is_enrollment', 'Enrollment'),
            ('is_monthly_fee', 'Fee'),
            ('is_uniform_fee', 'Uniform'),
            ('is_book', 'Book'),
            
        ], default='', states={'approved': [('readonly', True)]}
    )
    finance_line_ids = fields.One2many('ems.finance.enrollment.line', 'finance_id', states={'approved': [('readonly', True)]})
    finance_month_line_ids = fields.One2many('ems.finance.month.line', 'finance_id', states={'approved': [('readonly', True)]})
    finance_uniform_line_ids = fields.One2many('ems.finance.uniform.line', 'finance_id', states={'approved': [('readonly', True)]})
    finance_book_line_ids = fields.One2many('ems.finance.book.line', 'finance_id', states={'approved': [('readonly', True)]})
    enrollment_total = fields.Integer(readonly=True)
    fee_total = fields.Integer(readonly=True)
    uniform_total = fields.Integer(readonly=True)
    book_total = fields.Integer(readonly=True)
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('approved', 'Approved'),
        ], 'Status', default='draft', readonly=True,
        help='Choose whether the investment is still approved or not')
    MONTH_NAMES = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }
    

    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('ems.finance.sequence')
        return super(EmsFinance, self).create(vals)
    

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
   
    def action_approved(self):
        for rec in self:
            existing_record = self.search([
                ('student_id', '=', rec.student_id.id),
                ('date', '>=', rec.date.replace(day=1)),
                ('date', '<', (datetime.combine(rec.date, datetime.min.time()) + relativedelta(months=1)).date()),
                ('state', '=', 'approved'),
            ])
            if existing_record:
                existing_month_name = self.MONTH_NAMES.get(rec.finance_month_line_ids.month, 'Unknown')
                raise ValidationError(f"The student {rec.student_id.name} has already paid the fee for the {existing_month_name} month.")

            if rec.invoice_type == 'is_uniform_fee':
                for line in rec.finance_uniform_line_ids:
                    current_onhand = line.uniform_id.on_hand_quantity
                    line.uniform_id.write({'on_hand_quantity': current_onhand - line.pices})
                    if line.uniform_id.on_hand_quantity < line.pices:
                        raise ValidationError(f"Sorry! you have not enough {line.uniform_id.name} to sale")
                
            if rec.invoice_type == 'is_book':
                for line in rec.finance_book_line_ids:
                    current_onhand = line.book_id.on_hand_quantity
                    line.book_id.write({'on_hand_quantity': current_onhand - line.quantity})
                    if line.book_id.on_hand_quantity < line.quantity:
                        raise ValidationError(f"Sorry! you have not enough {line.book_id.name} to sale")

            if rec.invoice_type == 'is_enrollment':
                for line in rec.finance_line_ids:
                    book_current_onhand = line.book_id.on_hand_quantity
                    uniform_current_onhand = line.uniform_id.on_hand_quantity
                    line.book_id.write({'on_hand_quantity': book_current_onhand - line.book_quantity})
                    line.uniform_id.write({'on_hand_quantity': uniform_current_onhand - line.uniform_pices})
                    
                    if line.book_id.on_hand_quantity < line.book_quantity:
                        raise ValidationError(f"Sorry! you have not enough {line.book_id.name} to sale")
                    if  line.uniform_id.on_hand_quantity < line.uniform_pices :
                        raise ValidationError(f"Sorry! you have not enough {line.uniform_id.name} to sale")
                
 

            self.write({"state":"approved"})
        
    @api.constrains('finance_line_ids')
    def _total_enrollment_bill(self):
        if any(self.finance_line_ids):
            total = 0
            for line in self.finance_line_ids:
                total = total + line.total
            self.enrollment_total = total

    @api.constrains('finance_month_line_ids')
    def _total_fee_bill(self):
        if any(self.finance_month_line_ids):
            total = 0
            for line in self.finance_month_line_ids:
                total = total + line.total
            self.fee_total = total

    @api.constrains('finance_uniform_line_ids')
    def _total_uniform_bill(self):
        if any(self.finance_uniform_line_ids):
            total = 0
            for line in self.finance_uniform_line_ids:
                total = total + line.total
            self.uniform_total = total

    @api.constrains('finance_book_line_ids')
    def _total_book_bill(self):
        if any(self.finance_book_line_ids):
            total = 0
            for line in self.finance_book_line_ids:
                total = total + line.total
 
            self.book_total = total


    @api.model
    def create_monthly_invoices(self):
        current_date = fields.Date.today()
        current_month = current_date.month
        paid_student_ids = self.env['ems.finance.month.line'].search([
            ('month', '=', current_month),
            ('finance_id.invoice_type', '=', 'is_monthly_fee'),
        ]).mapped('finance_id.student_id.id')
        unpaid_students = self.env['ems.student'].search([('id', 'not in', paid_student_ids)])
        for student in unpaid_students:
            if student.id not in paid_student_ids:
                invoice_vals = {
                    'student_id': student.id,
                    'student_class': student.class_id.id,
                    'date': current_date,
                    'invoice_type': 'is_monthly_fee',
                }
                self.env['ems.finance'].create(invoice_vals)
        return True


 

class EmsFinanceEnrollmentLine(models.Model):
    _name = 'ems.finance.enrollment.line'
    _description = 'ems finance description'


    uniform_id = fields.Many2one('product.template', domain=[('is_uniform', '=', True)])
    uniform_pices = fields.Integer()
    uniform_price = fields.Integer()
    book_id = fields.Many2one('product.template', domain=[('is_book', '=', True)])
    book_quantity = fields.Integer()
    book_price = fields.Integer()
    registration_fee = fields.Integer()
    monthly_fee = fields.Integer()
    total = fields.Integer(compute="_compute_enrollment_total")
    finance_id = fields.Many2one('ems.finance')
    discount_amount = fields.Integer(related="finance_id.student_id.discount_id.discount_amount")


    @api.depends('registration_fee', 'monthly_fee', 'uniform_pices', 'uniform_price', 'book_price', 'book_quantity', 'discount_amount')
    def _compute_enrollment_total(self):
        for rec in self:
            total_before_discount = (rec.registration_fee) + (rec.monthly_fee) + (rec.uniform_pices * rec.uniform_price) + (rec.book_quantity * rec.book_price)
            total_after_discount = total_before_discount - (total_before_discount * (rec.discount_amount / 100))
            rec.total = total_after_discount

class EmsFinanceMonthLine(models.Model):
    _name = 'ems.finance.month.line'
    _description = 'ems finance month description'


    monthly_fee = fields.Integer()
    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], string='Month')
    finance_id = fields.Many2one('ems.finance')
    discount_amount = fields.Integer(related="finance_id.student_id.discount_id.discount_amount")
    total = fields.Integer(compute="_compute_month_total")
   
    @api.depends('monthly_fee',  'discount_amount')
    def _compute_month_total(self):
        for rec in self:
            total_after_discount = rec.monthly_fee  - (rec.monthly_fee  * (rec.discount_amount / 100))
            rec.total = total_after_discount

class EmsFinanceUniformLine(models.Model):
    _name = 'ems.finance.uniform.line'
    _description = 'ems finance uniform description'


    pices = fields.Integer()
    price = fields.Integer()
    total = fields.Integer(compute="_compute_uniform_total")
    
    finance_id = fields.Many2one('ems.finance')
    uniform_id = fields.Many2one('product.template', domain=[('is_uniform', '=', True)])
    @api.depends('price', 'pices')
    def _compute_uniform_total(self):
        for rec in self:
            rec.total = rec.price * rec.pices




class EmsFinanceBookLine(models.Model):
    _name = 'ems.finance.book.line'
    _description = 'ems finance book description'


    book_id = fields.Many2one('product.template', domain=[('is_book', '=', True)])
    quantity = fields.Integer()
    price = fields.Integer()
    total = fields.Integer(compute="_compute_book_total")
    finance_id = fields.Many2one('ems.finance')
    
    @api.depends('price', 'quantity')
    def _compute_book_total(self):
        for rec in self:
            rec.total = rec.price * rec.quantity
