from odoo import models, fields

class Cassier(models.Model):
    _name = 'kickapp.cassier'
    _description = 'Cassier'
    _inherit=['mail.thread','mail.activity.mixin'] # Pour les notifications par mail


    name = fields.Char(string='Nom', required=True)


