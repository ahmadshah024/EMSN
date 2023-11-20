# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EmsAassignment(models.Model):
    _name = 'ems.assignment'
    _description = 'ems assignment description'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher','=',True)], states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    class_id = fields.Many2one('ems.class.room', states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    subject_id = fields.Many2one('ems.subject', states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    assign_date = fields.Date(default=fields.Date.today(), states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    due_date = fields.Date(states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    submission_type = fields.Selection([('handwritten','Handwritten'),('hardcopy','Hardcopy'),('submite','Submite')], states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    file = fields.Binary('Attache Home', states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    state = fields.Selection([('active','Active'),('done','Done'),('draft','Draft')], default='draft')
    submitted_date = fields.Date()
    documents = fields.Binary()
    assignment_line_ids = fields.One2many('ems.assignment.line', 'assignment_id')

    def action_active(self):
        for rec in self:
            rec.state = 'active'

    def action_done(self):
        for rec in self:
            if rec.due_date and rec.due_date < fields.Date.today():
                raise UserError("Cannot change state to 'done' before the due date.")
            rec.state = 'done'

    def check_due_date(self):
        today = fields.Date.today()
        overdue_assignments = self.search([('state', '=', 'active'), ('due_date', '<=', today)])
        overdue_assignments.write({'state': 'done'})
    # def check_due_date(self):
    #     today = fields.Date.today()
    #     overdue_assignments = self.search([('state', '=', 'active'), ('due_date', '<', today)])
    #     overdue_assignments.write({'state': 'done'})
    
    
    @api.model
    def create(self, values):
        assignment = super(EmsAassignment, self).create(values)
        for student in assignment.class_id.student_ids:
            assignment._create_activity_for_student('mail_acitvity_student_assignment', student.user_id.id, 'an assignment is assigned to you')
        return assignment

    def _create_activity_for_student(self, mail_template_id, user, note):
        for rec in self:
            rec.activity_schedule(mail_template_id, user_id = user, note = note)
 

class EmsAassignmentLine(models.Model):
    _name = 'ems.assignment.line'
    _description = 'ems assignment line description'

    assignment_id = fields.Many2one('ems.assignment')
    submitted_date = fields.Date()
    documents = fields.Binary()
    student_id = fields.Many2one('ems.student')

