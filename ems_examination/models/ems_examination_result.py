from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmsExaminationResult(models.Model):
    _name = 'ems.examination.result'
    _description = 'ems_examination_result'

    student_id = fields.Many2one('ems.student', required=True)
    class_id = fields.Many2one(related='student_id.class_id')
    reference = fields.Char(related='student_id.reference')
    exam_type = fields.Selection([
        ('mid-term', 'Mid-term'),
        ('final', 'Final'),
    ], required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft')
    examination_result_line_ids = fields.One2many('ems.examination.result.line', 'examination_result_id')

    present_days = fields.Integer(related='student_id.present_count')
    absent_days = fields.Integer(related='student_id.absent_count')
    leave_days = fields.Integer(related='student_id.leave_count')
    total_marks = fields.Integer(compute='_compute_total_marks', store=True)
    average_marks = fields.Float(compute='_compute_average_marks', store=True)
    result = fields.Char(compute='_compute_result', store=True)
    grade = fields.Char(compute='_compute_grade', store=True)

    @api.depends('examination_result_line_ids', 'exam_type')
    def _compute_total_marks(self):
        for rec in self:
            total_marks = sum(rec.examination_result_line_ids.mapped('obtain_mark'))
            rec.total_marks = total_marks

    @api.depends('examination_result_line_ids', 'total_marks')
    def _compute_average_marks(self):
        for rec in self:
            subject_count = len(rec.examination_result_line_ids)
            if subject_count:
                rec.average_marks = rec.total_marks / subject_count
            else:
                rec.average_marks = 0.0

    @api.depends('exam_type', 'average_marks')
    def _compute_result(self):
        for rec in self:
            if rec.exam_type == 'mid-term':
                if rec.average_marks < (16 / 40 * 100):
                    rec.result = 'Fail'
                else:
                    rec.result = 'Pass'
            elif rec.exam_type == 'final':
                if rec.average_marks < (40 / 100 * 100):
                    rec.result = 'Fail'
                else:
                    rec.result = 'Pass'
            else:
                rec.result = ''

    @api.depends('average_marks')
    def _compute_grade(self):
        for rec in self:
            if 90 <= rec.average_marks <= 100:
                rec.grade = 'A+'
            elif 80 <= rec.average_marks < 90:
                rec.grade = 'A'
            elif 70 <= rec.average_marks < 80:
                rec.grade = 'B'
            elif 60 <= rec.average_marks < 70:
                rec.grade = 'C'
            elif 40 <= rec.average_marks < 60:
                rec.grade = 'D'
            else:
                rec.grade = 'F'










    
    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'  
            

    @api.onchange('class_id')
    def _onchange_class_id(self):
        for rec in self:
            if rec.class_id:
                class_subjects = rec.class_id.class_line_ids
                rec.examination_result_line_ids = [(5, 0, 0)]
                new_lines = [(0, 0, {'subject_id': subject.subject_id.id}) for subject in class_subjects]
                rec.examination_result_line_ids = new_lines
            else:
                rec.examination_result_line_ids = False
    

class EmsExaminationResultLine(models.Model):
    _name = 'ems.examination.result.line'
    _description = 'ems_examination_result.line'

    subject_id = fields.Many2one('ems.subject')
    max_mark = fields.Integer(related='subject_id.maximum_mark')
    min_mark = fields.Integer(related='subject_id.minimum_mark')
    obtain_mark = fields.Integer()
    examination_result_id = fields.Many2one('ems.examination.result')

