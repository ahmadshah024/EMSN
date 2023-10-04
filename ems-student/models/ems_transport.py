# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTransport(models.Model):
    _inherit = 'ems.transport'

    student_ids = fields.One2many('ems.student','transport_id', states={'done': [('readonly', True)]})
    student_name = fields.Char(related='student_ids.name', states={'done': [('readonly', True)]})