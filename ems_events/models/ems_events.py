# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsEvent(models.Model):
    _name = 'ems.event'
    _description = 'ems event'

    name = fields.Char(required=True)
    reason = fields.Text()
    event_category = fields.Selection([
        ('academic','Academic'),
        ('sports','Sports'),
        ('cultural','Cultural'),
        ('community','Community'),
        ('graduation','Graduation'),
        ('parent_teacher','Parent-Teacher'),
        ('art_and_Craft_exhibitions','Art and Craft Exhibitions'),
        ('science_fairs','Science Fairs'),
        ('special_celebrations','Special Celebrations'),
        ('workshops_and_training','Workshops and Training'),
    ])
