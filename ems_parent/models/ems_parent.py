                                                                                                                                                                
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime


class EmsParent(models.Model):
    _name = 'ems.parent'
    _description = 'Parent'

    name = fields.Char(states={'done': [('readonly', True)]}, required=True)
    image = fields.Binary(states={'done': [('readonly', True)]})
    address = fields.Char(states={'done': [('readonly', True)]})
    phone = fields.Char(states={'done': [('readonly', True)]}, required=True)
    email = fields.Char(states={'done': [('readonly', True)]}, required=True)
    dob = fields.Date(states={'done': [('readonly', True)]})
    age = fields.Char(compute='_compute_age', store=True, states={'done': [('readonly', True)]})
    user_id = fields.Many2one('res.users', copy=False, string="Related User") 
    partner_id = fields.Many2one('res.partner', copy=False, string="Related Partner", readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    relation = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('uncle', 'Uncle'),   
    ], states={'done': [('readonly', True)]}, required=True)
    job = fields.Char(states={'done': [('readonly', True)]})
    languages = fields.Many2one('res.lang',states={'done': [('readonly', True)]})
    # child = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'done': [('readonly', True)]}) 


 
    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    
    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'        


    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = False
            if rec.dob:
                if rec.dob > datetime.today().date():
                    raise ValidationError("Invalid date of birth, Please choose a date equal or older than today.")
                today = date.today()
                dob = rec.dob
                rec.age = today.year - dob.year - \
                    ((today.month, today.day) < (dob.month, dob.day))        

    def create_user_server_action(self):
        if not self.env.user.has_group('ems_parent.group_parent_administrator'):
            raise ValidationError("You cannot access this action.")

        for parent in self.browse(self.env.context['active_ids']):
            if not parent.user_id:
                partner_vals = {
                    'is_company': False,
                    'company_type': 'person',
                    'name': parent.name or ('Unknown'),
                    'email': parent.email or '',
                    'phone': parent.phone or '',
                    'image_1920': parent.image,
                }
                new_partner_id = self.env['res.partner'].create(partner_vals)
                new_user_id = self.env['res.users'].create({
                    'partner_id': new_partner_id.id,
                    'login': parent.email or parent.name,
                })
                parent.write({
                    'user_id': new_user_id.id,
                    'partner_id': new_partner_id.id,
                })
                self.env.ref('ems_parent.group_parent_user').users = [(4, new_user_id.id)]

        return True