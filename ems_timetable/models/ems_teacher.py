# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTeacher(models.Model):
    _inherit = 'hr.employee'


    subject_ids = fields.Many2many('ems.subject')