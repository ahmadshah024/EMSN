from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmsExaminationResult(models.Model):
    _name = 'ems.examination.result'
    _description = 'ems_examination_result'

    student_id = fields.Many2one('ems.student')
    class_id = fields.Many2one(related='student_id.class_id')
    reference = fields.Char(related='student_id.reference')
    exam_type = fields.Selection([
        ('mid-term', 'Mid-term'),
        ('final', 'Final'),
    ])
    examination_result_line_ids = fields.One2many('ems.examination.result.line', 'examination_result_id')


    @api.depends('class_id')
    def _compute_subject_id(self):
        for record in self:
            if record.class_id:
                students = record.class_id.subject_id
                record.ems_examination_result_line_ids = [(0, 0, {'subject_id': student.id}) for student in students]
            else:
                record.ems_examination_result_line_ids = False


class EmsExaminationResultLine(models.Model):
    _name = 'ems.examination.result.line'
    _description = 'ems_examination_result.line'

    subject_id = fields.Many2one('ems.subject')
    class_id = fields.Many2one(related='student_id.class_id')
    examination_result_id = fields.Many2one('ems.examination.result')