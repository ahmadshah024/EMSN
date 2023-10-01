# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date



class EmsStudent(models.Model):
    _name = 'ems.student'
    _description = 'ems student description'

    reference = fields.Char("Reference No", required=True,copy=False,readonly=True,default='New' )
    image = fields.Binary()
    name = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})

    father_name = fields.Char(required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    grand_father_name = fields.Char(required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    address = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    phone = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    email = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    nic = fields.Char('Tazkira No', required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    dob = fields.Date(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    age = fields.Char(compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    parent_id = fields.Many2one('ems.parent', required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    school = fields.Many2one('res.company', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    class_name = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    academic_year = fields.Date(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    date = fields.Date(default=lambda self: fields.Date.today(),states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    parent_name = fields.Char(related='parent_id.name', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_name = fields.Char('School Name',states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_registration_no = fields.Char('Registration No', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_addmission_date = fields.Date('Addmission Date', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_exit_date = fields.Date('Exit Date', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_exit_reason = fields.Text(states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    remarks = fields.Html()
    award_ids = fields.One2many('ems.student.award','student_id', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    certificate_ids = fields.One2many('ems.student.certificate','student_id', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled'), ('graduate', 'Graduated'), ('change','Changed')], default='draft')

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_graduate(self):
        for rec in self:
            rec.state = 'graduate'
        
    def action_change(self):
        for rec in self:
            rec.state = 'change'
    
    _sql_constraints = [
        ('name_unique', 'unique(nic)',
         "Please Check the NIC Number, already exists!"),
    ]
    

    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.student.sequence')
        return super(EmsStudent, self).create(vals)
    

    @api.depends('dob')
    def _compute_age(self):
        for patient in self:
            patient.age = False
            if patient.dob:
                if patient.dob > datetime.today().date():
                    raise ValidationError("Invalid date of birth, Please choose a date equal or older than today.")
                today = date.today()
                dob = patient.dob
                patient.age = today.year - dob.year - \
                    ((today.month, today.day) < (dob.month, dob.day))


class Parent(models.Model):
    _name = 'ems.parent'
    _description = 'ems parent description'


    name = fields.Char()


class EmsStudentAward(models.Model):
    _name = 'ems.student.award'
    _description = 'ems student award description'


    name = fields.Char()
    description = fields.Text()

    student_id = fields.Many2one('ems.student')

class EmsStudentCertificate(models.Model):
    _name = 'ems.student.certificate'
    _description = 'ems student certificate description'


    certificate = fields.Binary()
    description = fields.Text()

    student_id = fields.Many2one('ems.student')
