# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError                     

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
    


    def generate_timetable(self):
        # if self.state != 'draft':
        #     raise UserError('Timetable can only be generated in draft state.')

        self.timetable_line_ids.unlink()  # Clear existing lines

        # Get all necessary data
        all_teachers = self.teacher_ids
        all_classes = self.class_ids
        all_subjects = self.subject_ids
        all_days = self.day_ids

        # Generate teacher subject-class combinations
        teacher_combinations = self._get_teacher_subject_class_combinations(all_teachers, all_classes, all_subjects)

        # Schedule the classes
        self._schedule_classes(all_days, all_classes, teacher_combinations)

        # Change the state to 'done'
        self.write({'state': 'done'})

    def _get_teacher_subject_class_combinations(self, all_teachers, all_classes, all_subjects):
        combinations = []
        for teacher in all_teachers:
            # Let's assume each teacher has a 'subject_lines' field which tells us what they teach
            for line in teacher.teacher_line_ids:
                if line.subject_id in all_subjects and line.class_id in all_classes:
                    # Each line would tell us how many periods per week and to which class
                    for _ in range(line.period_count):
                        combinations.append({
                            'teacher': teacher,
                            'subject': line.subject_id,
                            'class': line.class_id,
                        })
        return combinations

    def _schedule_classes(self, all_days, all_classes, teacher_combinations):
    # Schedule each class for each day
        for day in all_days:
            for class_group in all_classes:
                # Assuming that 'periods_per_day' is the field that holds the number of periods per day
                for period in range(1, self.period_count + 1):
                    # This logic assumes that you have to go through each teacher_combination to find one that can be scheduled
                    # for the current class_group and period. You will need a more sophisticated algorithm for complex scheduling.
                    for combination in list(teacher_combinations):  # Make a copy of the list for safe iteration
                        if self._can_schedule(combination, day, class_group):
                            # Create a timetable line record with the scheduled class details
                            self.env['ems.timetable.line'].create({
                                'timetable_id': self.id,
                                'day_id': day.id,
                                'period_number': period,  # Assuming you have a field to store the period number
                                'teacher_id': combination['teacher'].id,
                                'class_id': class_group.id,
                                'subject_id': combination['subject'].id,
                            })
                            # Once a teacher is scheduled for a class in a period, they cannot be scheduled again in the same period
                            teacher_combinations.remove(combination)
                            break
    def _can_schedule(self, combination, day, class_group):
    # Check if the teacher is already scheduled for this day and period
        teacher_scheduled = self.env['ems.timetable.line'].search([
            ('day_id', '=', day.id),
            ('teacher_id', '=', combination['teacher'].id),
            # You might have a 'period' field to check here
        ], limit=1)

        # Check if the class has reached its maximum number of periods for the subject this week
        subject_period_count = self.env['ems.timetable.line'].search_count([
            ('class_id', '=', class_group.id),
            ('subject_id', '=', combination['subject'].id),
            # Assuming there is a relation to the whole week, not just a single day
        ])

        # Assuming each 'subject_line' has a 'period_count' field indicating the max periods per week
        # max_periods_for_subject = combination['subject'].subject_lines.filtered(
        #     lambda l: l.class_id == class_group).period_count
        # max_periods_for_subject = self._get_period_count_for_class_subject(class_group, combination['subject'])
        # The teacher is available if they are not already scheduled for this day and period
        teacher_available = not teacher_scheduled

        # The class has not exceeded its maximum number of periods for this subject
        # class_has_room = subject_period_count < max_periods_for_subject

        # return teacher_available and class_has_room

    # def _get_period_count_for_class_subject(self, class_group, subject):
    # # This is a pseudo-code. You should replace 'class.subject.relation' with the actual name of your relationship model
    # # and adjust the domain accordingly to match your model's fields and logic.
    #     relation = self.env['class.subject.relation'].search([
    #         ('class_id', '=', class_group.id),
    #         ('subject_id', '=', subject.id),
    #     ], limit=1)
    #     return relation.period_count if relation else 0
    # def generate_timetable(self):
    #     if self.state != 'draft':
    #         raise UserError('Timetable can only be generated in draft state.')

    #     self.timetable_line_ids.unlink()  # Clear existing lines

    #     # Get all necessary data
    #     all_teachers = self.teacher_ids
    #     all_classes = self.class_ids
    #     all_subjects = self.subject_ids
    #     all_days = self.day_ids
    #     # ... your existing code ...

    #     # Generate teacher subject-class combinations
    #     teacher_combinations = self._get_teacher_subject_class_combinations(all_teachers, all_classes, all_subjects)

    #     # Schedule the classes
    #     self._schedule_classes(all_days, all_classes, teacher_combinations)

    #     # Change the state to done
    #     self.action_done()

    # def _get_teacher_subject_class_combinations(self, all_teachers, all_classes, all_subjects):
    #     # This is a placeholder. You will need to fetch and return all valid
    #     # combinations of teachers, subjects, and classes.
    #     combinations = [
    #         # Assuming each combination is a dictionary like:
    #         # {'teacher': teacher_record, 'subject': subject_record, 'class': class_record}
    #         # You need to populate this list with actual records from your system.
    #     ]
    #     return combinations

    # def _schedule_classes(self,all_days, all_classes, teacher_combinations):
    #     for class_group in self.class_ids:
    #         for day in self.day_ids:
    #             # You could sort or filter teacher_combinations here based on some criteria.
    #             for combination in teacher_combinations:
    #                 # This is a very naive approach, just to illustrate:
    #                 # You need to add logic here to check if the teacher is available
    #                 # for this class_group and day, and if the period_count allows for it.
    #                 if self._can_schedule(combination, day, class_group):
    #                     self.env['ems.timetable.line'].create({
    #                         'timetable_id': self.id,
    #                         # Assign the fields from the combination to the timetable line
    #                         'teacher_id': combination['teacher'].id,
    #                         'subject_id': combination['subject'].id,
    #                         'class_id': combination['class'].id,
    #                         'day_id': day.id,
    #                     })

    
    
class EmsTimetableLine(models.Model):
    _name = 'ems.timetable.line'
    _description = 'ems timetable line description'




    day_id = fields.Many2one('ems.day', string='Day', required=True)
    # period_id = fields.Many2one('ems.period', string='Period', required=True)
    period = fields.Integer()
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)], required=True)
    class_id = fields.Many2one('ems.class.room', required=True)
    subject_id = fields.Many2one('ems.subject', required=True)
    timetable_id = fields.Many2one('ems.timetable', ondelete='cascade', required=True)
    # day = fields.Selection([
    #     ('saturday','Saturday'),
    #     ('sunday','Sunday'),
    #     ('monday','Monday'),
    #     ('tuesday','Tuesday'),
    #     ('wednesday','Wednesday'),
    #     ('thursday','Thursday'),
    # ])
    # teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)])
    # class_id = fields.Many2one('ems.class.room')
    # subject_id = fields.Many2one('ems.subject')

 
    
    timetable_id = fields.Many2one('ems.timetable')

    # subject_ids = fields.Many2many('ems.subject', string='Subjects', compute='_compute_subjects')
    # timetable_id = fields.Many2one('ems.timetable')
 
             


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
