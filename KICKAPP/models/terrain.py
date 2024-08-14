from typing import AsyncGenerator
from odoo import models, fields, api

#terrain
class kickappTerrain(models.Model):
    _name = 'kickapp.terrain'
    _description = 'Gestion des Terrains de Football'
    _inherit=['mail.thread','mail.activity.mixin'] # Pour les notifications par mail

    name = fields.Char(string='Nom du Terrain', required=True)
    available = fields.Boolean(string='Disponible' )
    capacity = fields.Integer(string='Capacité du Terrain')
    category = fields.Selection([
        ('adulte', 'Adulte'),
        ('enfant', 'Enfant'),
    ], string='Catégorie')
    type = fields.Selection([
        ('football', 'Football'),
        ('tennis', 'Tennis'),
        ('handball', 'Handball'),
        ('basketball', 'Basketball'),
        # Ajoutez d'autres types au besoin
    ], string='Type')