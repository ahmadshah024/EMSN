# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class EmsStudent(models.Model):
    _inherit = 'ems.student'

    attendance_id = fields.Many2one('ems.attendance')
    is_present = fields.Boolean(default=True, attrs="{'readonly': [('is_present', '=', True)]}")
    is_absent = fields.Boolean(default=False, attrs="{'readonly': [('is_absent', '=', True)]}")
    is_leave = fields.Boolean(default=False, attrs="{'readonly': [('is_leave', '=', True)]}")
    

    @api.onchange('is_present')
    def _onchange_is_present(self):
        if self.is_present:
            self.is_absent = self.is_leave = False

            

    @api.onchange('is_absent')
    def _onchange_is_absent(self):
        if self.is_absent:
            self.is_present = self.is_leave = False

    @api.onchange('is_leave')
    def _onchange_is_leave(self):
        if self.is_leave:
            self.is_absent = self.is_present = False

    
        