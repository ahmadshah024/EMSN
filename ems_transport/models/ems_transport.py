# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTransport(models.Model):
    _name = 'ems.transport'
    _description = 'ems transport description'

    name = fields.Char(readonly=True, default='New')
    distanation = fields.Char(required=True)
    car_id = fields.Many2one('ems.transport.car')
    driver_id = fields.Many2one('ems.transport.driver')
    


     


class EmsTransportCar(models.Model):
    _name = 'ems.transport.car'
    _description = 'ems transport car description'

    name = fields.Char()
    modle = fields.Char()
    no_palette = fields.Char()

    


class EmsTransportDriver(models.Model):
    _name = 'ems.transport.driver'
    _description = 'ems transport driver description'

    name = fields.Char()
    father_name = fields.Char()
    nic = fields.Char()
    phone = fields.Char()

    