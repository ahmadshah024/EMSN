# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTimetable(models.Model):
    _name = 'ems.timetable'
    _description = 'ems timetable'

    name = fields.Char(states={'done': [('readonly', True)]}, required=True)
    academic_year = fields.Date(states={'done': [('readonly', True)]})
    class_ids = fields.Many2many('ems.class.room', states={'done': [('readonly', True)]}, required=True)
    class_id = fields.Many2one('ems.class.room')
    day_ids = fields.Many2many('ems.timetable.day')
    period_count = fields.Integer('Period Per Week')
    subject_ids = fields.Many2many('ems.subject')
    teacher_ids = fields.Many2many('hr.employee', domain=[('is_teacher', '=', True)])
    # class_ids = fields.Many2many('ems.class.room', states={'done': [('readonly', True)]}, required=True)
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)
    timetable_line_ids = fields.One2many('ems.timetable.line','timetable_id', states={'done': [('readonly', True)]})



    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


    
    
    
class EmsTimetableLine(models.Model):
    _name = 'ems.timetable.line'
    _description = 'ems timetable line description'

    day = fields.Selection([
        ('saturday','Saturday'),
        ('sunday','Sunday'),
        ('monday','Monday'),
        ('tuesday','Tuesday'),
        ('wednesday','Wednesday'),
        ('thursday','Thursday'),
    ])
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)])
    class_id = fields.Many2one('ems.class.room')
    subject_id = fields.Many2one('ems.subject')


    subject_id1 = fields.Many2one('ems.subject')
    subject_id2 = fields.Many2one('ems.subject')
    subject_id3 = fields.Many2one('ems.subject')
    subject_id4 = fields.Many2one('ems.subject')
    subject_id5 = fields.Many2one('ems.subject')
    subject_id6 = fields.Many2one('ems.subject')
    subject_id7 = fields.Many2one('ems.subject')
    subject_id8 = fields.Many2one('ems.subject')
    subject_id9 = fields.Many2one('ems.subject')
    
    
    timetable_id = fields.Many2one('ems.timetable')

    subject_ids = fields.Many2many('ems.subject', string='Subjects', compute='_compute_subjects')
    timetable_id = fields.Many2one('ems.timetable')

    # @api.depends('timetable_id.subject_count')
    # def _compute_subjects(self):
    #     for record in self:
             


class EmsTimetablePeriod(models.Model):
    _name = 'ems.timetable.period'
    _description = 'ems timetable period description'


    name = fields.Char()

    period_line_ids = fields.One2many('ems.timetable.period.line', 'period_id')


class EmsTimetablePeriodLine(models.Model):
    _name = 'ems.timetable.period.line'
    _description = 'ems timetable period line description'


    number = fields.Integer('No')
    start_time = fields.Float()
    end_time = fields.Float()
    length = fields.Float(compute="_compute_length")
    period_id = fields.Many2one('ems.timetable.period')





    @api.depends('start_time', 'end_time')
    def _compute_length(self):
        for rec in self:
            start_time_minutes = int(rec.start_time) * 60 + (rec.start_time - int(rec.start_time)) * 100
            end_time_minutes = int(rec.end_time) * 60 + (rec.end_time - int(rec.end_time)) * 100

            rec.length = end_time_minutes - start_time_minutes


class EmsTimetableDay(models.Model):
    _name = 'ems.timetable.day'
    _description = 'ems timetable day description'


    name = fields.Char()
    
    day_line_ids = fields.One2many('ems.timetable.day.line', 'day_id')


class EmsTimetableDayLine(models.Model):
    _name = 'ems.timetable.day.line'
    _description = 'ems timetable day line description'


    name = fields.Char()

    day_id = fields.Many2one('ems.timetable.day')    
