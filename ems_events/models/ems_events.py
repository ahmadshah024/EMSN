# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmsEvent(models.Model):
    _name = 'ems.event'
    _description = 'ems event'
    _inherit = 'mail.thread'

    name = fields.Char(required=True, states={'done': [('readonly', True)]})
    reason = fields.Text(states={'done': [('readonly', True)]})
    date =fields.Date(states={'done': [('readonly', True)]})
    teacher_id = fields.Many2one('hr.employee', states={'done': [('readonly', True)]}, domain=[('is_teacher','=', True)])
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)

    event_category = fields.Selection([
        ('academic','Academic'),
        ('sports','Sports'),
        ('cultural','Cultural'),
        ('community','Community'),
        ('graduation','Graduation'),
        ('parent_teacher','Parent-Teacher'),
        ('art_and_Craft_exhibitions','Art and Craft Exhibitions'),
        ('science_fairs','Science Fairs'),
        ('special_celebrations','Special Celebrations'),
        ('workshops_and_training','Workshops and Training'),
    ], states={'done': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')
    event_line_ids = fields.One2many('ems.event.line', 'event_id')



    def action_done(self):
        for rec in self:
            rec.state = 'done'
            # Send emails to students and teachers
            rec.send_notification_emails()

    def send_notification_emails(self):
        for rec in self:
            student = rec.event_line_ids.student_id
            teacher = rec.teacher_id
            student_email_template = rec.env.ref('ems_events.mail_template_ems_event_student', raise_if_not_found=False)
            teacher_email_template = rec.env.ref('ems_events.mail_template_ems_event_teacher', raise_if_not_found=False)
            if student:
                if not student.email:
                    raise ValidationError('please configure email to the Student')
                student_email_template.email_to = student.email
                student_email_template.send_mail(rec.id, force_send=True)
            if teacher:
                if not teacher.work_email:
                    raise ValidationError('please configure email to the Teacher')
                teacher_email_template.email_to = teacher.work_email
                teacher_email_template.send_mail(rec.id, force_send=True)

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class EmsEventLine(models.Model):
    _name = 'ems.event.line'
    _description = 'ems event line'


    student_id = fields.Many2one('ems.student')
    father_name = fields.Char(related='student_id.father_name')
    class_id = fields.Many2one(related='student_id.class_id')
    phone = fields.Char(related='student_id.phone')
    
    
    event_id = fields.Many2one('ems.event')
    def send_student_notification_email(self):
        self.message_post_with_template(
            self.env.ref('ems_evnts.mail_template_ems_event_student').id,
            email_values={'email_to': self.student_id.email}
        )