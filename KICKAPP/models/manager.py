from odoo import models, fields

class Manager(models.Model):
    _name = 'kickapp.manager'
    _description = 'Manager'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Pour les notifications par mail


    name = fields.Char(string='Nom', required=True)