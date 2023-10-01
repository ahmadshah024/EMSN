
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime


class EmsParent(models.Model):
    _name = 'ems.parent'
    _description = 'ems_parent'

    name = fields.Char()
    image = fields.Binary()
    address = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    dob = fields.Date()
    age = fields.Char(compute='_compute_age', store=True)
    relation = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('uncle', 'Uncle'),   
    ])
    job = fields.Char()
    languages = fields.Many2one('res.lang')
    child = fields.Char()
    student_ids = fields.One2many('ems.student','parent_id')
    state = fields.Selection([
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='done', track_visibility='onchange')


 
    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    
    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'


    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = False
            if rec.dob:
                if rec.dob > datetime.today().date():
                    raise ValidationError("Invalid date of birth, Please choose a date equal or older than today.")
                today = date.today()
                dob = rec.dob
                rec.age = today.year - dob.year - \
                    ((today.month, today.day) < (dob.month, dob.day))        

class EmsStudent(models.Model):
    _name = 'ems.student'

     
    name = fields.Char()
    parent_id = fields.Many2one('ems.parent')