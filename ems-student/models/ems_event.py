# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

class EmsEvent(models.Model):
    _inherit = "ems.event"
    _description = 'ems event inherited  description'


    student_ids = fields.One2many('ems.student', 'event_id')