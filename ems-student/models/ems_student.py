# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date



class EmsStudent(models.Model):
    _name = 'ems.student'
    _description = 'ems student description'

    reference = fields.Char("Reference No", required=True,copy=False,readonly=True,default='New' )
    image = fields.Binary(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    name = fields.Char(states={'done': [('readonly', True)],'graduate': [('readonly', True)], 'change': [('readonly', True)]}, required=True)

    father_name = fields.Char(required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    grand_father_name = fields.Char(required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    address = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    phone = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    email = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    nic = fields.Char('Tazkira No', required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    dob = fields.Date(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    age = fields.Char(compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    student_document = fields.Binary(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    parent_id = fields.Many2one('ems.parent', required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    school = fields.Many2one('res.company', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    class_id = fields.Many2one('ems.class.room', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    country_id = fields.Many2one('res.country', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]}  ,default=lambda self: self.env['res.country'].search([('name', '=', 'Afghanistan'), ('code', '=', 'AF')]))
    province_id = fields.Many2one('res.country.state', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]} ,domain="[('country_id', '=', country_id)]", string="Province/State")
    district_id = fields.Many2one('ems.district', domain="[('province_id', '=', province_id)]", states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    academic_year = fields.Date(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    date = fields.Date(default=lambda self: fields.Date.today(),states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    parent_name = fields.Char(related='parent_id.name', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_name = fields.Char('School Name',states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_registration_no = fields.Char('Registration No', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_addmission_date = fields.Date('Addmission Date', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_exit_date = fields.Date('Exit Date', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_exit_reason = fields.Text(states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_document_file = fields.Binary('Documents')
    remarks = fields.Html(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    award_ids = fields.One2many('ems.student.award','student_id', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    certificate_ids = fields.One2many('ems.student.certificate','student_id', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled'), ('graduate', 'Graduated'), ('change','Changed')], default='draft')
    is_new = fields.Boolean('Is New', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    is_changed = fields.Boolean('Is Change', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})

    new_school = fields.Char(readonly=True)
    new_reason = fields.Char(readonly=True)
    new_school_date = fields.Date(readonly=True)
    documents = fields.Binary(readonly=True)


    def action_change_new_flase(self):
        for rec in self:
            if rec.is_new or rec.is_changed:
                rec.is_new = False
                rec.is_changed = False
                


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
        return {
        'type': 'ir.actions.act_window',
        'name': 'New School',
        'res_model': 'change.school.wizard',
        'view_type': 'form',
        'view_mode': 'form',
        'target': 'new',
        'context':{'default_student_id': self.id}
    }
    
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



    @api.model
    def create(self, vals):
        """Method to create user when student is created"""
        if vals.get("pid", _("New")) == _("New"):
            vals["pid"] = self.env["ir.sequence"].next_by_code(
                "student.student"
            ) or _("New")
        if vals.get("pid", False):
            vals["login"] = vals["pid"]
            vals["password"] = vals["pid"]
        else:
            raise UserError(
                _("Error! PID not valid so record will not be saved.")
            )
        if vals.get("company_id", False):
            company_vals = {"company_ids": [(4, vals.get("company_id"))]}
            vals.update(company_vals)
        if vals.get("email"):
            school.emailvalidation(vals.get("email"))
        res = super(StudentStudent, self).create(vals)
        teacher = self.env["school.teacher"]
        for data in res.parent_id:
            for record in teacher.search([("stu_parent_id", "=", data.id)]):
                record.write({"student_id": [(4, res.id, None)]})
        # Assign group to student based on condition
        emp_grp = self.env.ref("base.group_user")
        if res.state == "draft":
            admission_group = self.env.ref("school.group_is_admission")
            new_grp_list = [admission_group.id, emp_grp.id]
            res.user_id.write({"groups_id": [(6, 0, new_grp_list)]})
        elif res.state == "done":
            done_student = self.env.ref("school.group_school_student")
            group_list = [done_student.id, emp_grp.id]
            res.user_id.write({"groups_id": [(6, 0, group_list)]})
        return res
# class Parent(models.Model):
#     _name = 'ems.parent'
#     _description = 'ems parent description'


#     name = fields.Char()


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

class EmsClassRoom(models.Model):
    _name = 'ems.class.room'
    _description = 'ems class room description'


    name = fields.Char('Name', required=True)
    block = fields.Char('Block')
    room_number = fields.Char('Room Number')


