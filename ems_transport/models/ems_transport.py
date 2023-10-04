# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTransport(models.Model):
    _name = 'ems.transport'
    _description = 'ems transport description'

    name = fields.Char(readonly=True, default='New')
    distanation = fields.Char(required=True, states={'done': [('readonly', True)]})
    car_id = fields.Many2one('ems.transport.car', states={'done': [('readonly', True)]})
    driver_id = fields.Many2one('ems.transport.driver', states={'done': [('readonly', True)]})
    transport_fee = fields.Integer(required=True, default=None, states={'done': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')
    transport_line_ids = fields.One2many('ems.transport.line', 'transport_id')


    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('ems.transport.sequence')
        return super(EmsTransport, self).create(vals)
    
class EmsTransportline(models.Model):
    _name = 'ems.transport.line'
    _description = 'ems transport line description'


    student_id = fields.Many2one('ems.student')
    father_name = fields.Char(related='student_id.father_name')
    age = fields.Integer(related='student_id.age')
    transport_id = fields.Many2one('ems.transport')



class EmsTransportCar(models.Model):
    _name = 'ems.transport.car'
    _description = 'ems transport car description'

    name = fields.Char(readonly=True, default='New')
    model = fields.Char(required=True, states={'done': [('readonly', True)]})
    no_palette = fields.Char(required=True, states={'done': [('readonly', True)]})
    image = fields.Binary(states={'done': [('readonly', True)]})
    color = fields.Char(states={'done': [('readonly', True)]})
    car_document = fields.Binary(states={'done': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')



    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('ems.transport.car.sequence')
        return super(EmsTransportCar, self).create(vals)
    



class EmsTransportDriver(models.Model):
    _name = 'ems.transport.driver'
    _description = 'ems transport driver description'

    name = fields.Char(required=True, states={'done': [('readonly', True)]})
    father_name = fields.Char(states={'done': [('readonly', True)]})
    nic = fields.Char(required=True, states={'done': [('readonly', True)]})
    phone = fields.Char(required=True, states={'done': [('readonly', True)]})
    image = fields.Binary(states={'done': [('readonly', True)]})
    driving_license = fields.Binary(required=True, states={'done': [('readonly', True)]})
    car_id = fields.Many2one('ems.transport.car', states={'done': [('readonly', True)]})
    salary = fields.Integer(states={'done': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')



    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
    