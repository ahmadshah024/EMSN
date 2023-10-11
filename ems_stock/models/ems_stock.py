# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsStock(models.Model):
    _inherit = 'product.template'


    is_uniform = fields.Boolean()
    is_book = fields.Boolean()
    price = fields.Integer()