# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTransport(models.Model):
    _inherit = 'ems.transport'

    teacher_ids = fields.One2many('hr.employee','transport_id', states={'done': [('readonly', True)]})
