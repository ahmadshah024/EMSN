# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsExamination(models.Model):
    _name = 'ems.examination'
    _description = 'ems_examination'


    reference = fields.Char(readonly=True, default="New")
    name = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    academic_year = fields.Char()
    exam_type = fields.Selection([
        ('mid-term', 'Mid-term'),
        ('final', 'Final'),
    ], required=True)
    examination_line_ids = fields.One2many('ems.examination.line', 'examination_id')


    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.examination.sequence')
        return super(EmsExamination, self).create(vals)
   

class EmsExaminationLine(models.Model):
    _name = 'ems.examination.line'
    _description = 'ems_examination_line'



    class_id = fields.Many2one('ems.class.room')
    timetable_id = fields.Many2one('ems.exam.timetable')
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher','=', True)])
    examination_id = fields.Many2one('ems.examination')
