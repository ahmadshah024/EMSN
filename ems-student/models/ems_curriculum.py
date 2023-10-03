# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsCurriculum(models.Model):
    _inherit = 'ems.curriculum'

    class_id = fields.Many2one('ems.class.room')