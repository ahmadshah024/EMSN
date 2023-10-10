# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTimetable(models.Model):
    _name = 'ems.timetable'
    _description = 'ems timetable'

    name = fields.Char(states={'done': [('readonly', True)]}, required=True)
    academic_year = fields.Date(states={'done': [('readonly', True)]})
    class_id = fields.Many2one('ems.class.room', states={'done': [('readonly', True)]}, required=True)
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

    week_days = fields.Selection([
        ('saturday','Saturday'),
        ('sunday','Sunday'),
        ('monday','Monday'),
        ('tuesday','Tuesday'),
        ('wednesday','Wednesday'),
        ('thursday','Thursday'),
        ('friday','Friday'),
        ('break','Break'),
    ])
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
             