# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsEvent(models.Model):
    _name = 'ems.event'
    _description = 'ems event'

    name = fields.Char(required=True, states={'done': [('readonly', True)]})
    reason = fields.Text(states={'done': [('readonly', True)]})
    date =fields.Date(states={'done': [('readonly', True)]})
    teacher_id = fields.Many2one('hr.employee', states={'done': [('readonly', True)]})
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



    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'