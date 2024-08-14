from typing import AsyncGenerator
from odoo import models, fields, api

class kickappClub(models.Model):
    _name = 'kickapp.club'
    _description = 'Clubs du Football'
    _inherit=['mail.thread','mail.activity.mixin'] # Pour les notifications par mail




    name = fields.Char(string='Nom du Club', required=True)
    description = fields.Text(string='Description du Club')    
    coach_id = fields.Many2one('kickapp.coach', string='Entraîneur')
    players_ids = fields.One2many('kickapp.joueur', 'club_id', string='Joueurs du Club')
    image = fields.Binary(string='Logo du Club')
    club_type = fields.Selection([('Academy', 'Academy kick app '), ('bank', 'Club de Banque'),('simple', 'Club simple')], string='Type de Club', default='simple')
    event_ids = fields.One2many('kickapp.club.event', 'club_id', string='Events')
    has_events = fields.Boolean(string='Has Events', compute='_compute_has_events')
    has_unread_events = fields.Boolean(string='Has Unread Events', compute='_compute_unread_events')
    event_summary = fields.Html(string='Evenement', compute='_compute_event_summary')
    subscription_product_id = fields.Many2one('product.product', string='Produit d\'abonnement', help="Produit utilisé pour l'abonnement à ce club.")
    
    subscribers_count = fields.Integer(string='Nombre d\'abonnés', compute='_compute_subscribers_count', store=True)

   

    @api.depends('event_ids')
    def _compute_event_summary(self):
        for club in self:
            summary = '<ul>'
            for event in club.event_ids:
                summary += f'<li><strong>{event.name}</strong>: {event.start_datetime} - {event.end_datetime}</li>'
            summary += '</ul>'
            club.event_summary = summary


    @api.model
    def get_clubs_count(self):
        clubs_count = self.env['kickapp.club'].search_count([])
        return clubs_count
    

    @api.depends('event_ids')
    def _compute_unread_events(self):
        for club in self:
            club.has_unread_events = any(event.state == 'new' for event in club.event_ids)
            

    @api.depends('event_ids')
    def _compute_has_events(self):
        for club in self:
            club.has_events = bool(club.event_ids)      
            
    @api.depends('subscription_product_id')
    def _compute_subscribers_count(self):
        for club in self:
            club.subscribers_count = self.env['kickapp.club.subscription'].search_count([('club_id', '=', club.id), ('state', '=', 'paid')])  
  