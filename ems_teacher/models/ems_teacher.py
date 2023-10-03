# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

class EmsTeacher(models.Model):
    _inherit = "hr.employee"
    _description = 'ems teacher inherited  description'


    is_teacher = fields.Boolean("Is Teacher")
    work_phone = fields.Char(default="+93(0)7909900961")
    salary = fields.Integer("Salary")
    category_ids = fields.Many2many(placeholder='subjects')

