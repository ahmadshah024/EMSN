# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTeacher(models.Model):
    _inherit = 'hr.employee'


    day_id = fields.Many2one('ems.timetable.day')        

    teacher_availablility_ids = fields.One2many('ems.teacher.availability', 'teacher_id', compute='_compute_availablility_ids')


    # @api.onchange('day_id')
    # def _onchange_day_id(self):
    #     if self.day_id:
    #         # Clear existing teacher_availablility_ids
    #         self.teacher_availablility_ids = [(5, 0, 0)]

    #         # Create teacher availability records based on selected day
    #         days = self.day_id.day_line_ids
    #         teacher_availability_records = [(0, 0, {'day_id': day.id}) for day in days]
    #         self.teacher_availablility_ids = teacher_availability_records
    #     else:
    #         # Clear teacher_availablility_ids if no day is selected
    #         self.teacher_availablility_ids = [(5, 0, 0)]



    @api.depends('day_id')
    def _compute_availablility_ids(self):
        for record in self:
            if record.day_id:
                days = record.day_id.day_line_ids
                availability_records = [(0, 0, {})] * len(days)
                record.teacher_availablility_ids = availability_records
            else:
                record.teacher_availablility_ids = False 
    # @api.depends('day_id')
    # def _compute_availablility_ids(self):
    #     for record in self:
    #         if record.day_id:
    #             days = record.day_id.day_line_ids
    #             record.teacher_availablility_ids = [(0, 0, {'day_id': day.id}) for day in days]
    #         else:
    #             record.teacher_availablility_ids = False


class EmsTeacherAvailability(models.Model):
    _inherit = 'ems.teacher.availability'


    day_id = fields.Many2one('ems.timetable.day')
