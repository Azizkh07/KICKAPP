from odoo import models, fields
from odoo import api

class kickappEvaluation(models.Model):
    _name = 'kickapp.evaluation'
    _description = 'Évaluation des Joueurs'
    _inherit=['mail.thread','mail.activity.mixin'] # Pour les notifications par mail


    player_id = fields.Many2one('kickapp.joueur', string='Joueur', required=True)
    coach_id = fields.Many2one('kickapp.coach', string='Coach', required=True)
    speed = fields.Float(string='Vitesse', required=True)
    dribbling = fields.Float(string='Dribble', required=True)
    matches_played = fields.Integer(string='Matchs Joués', required=True)
    goals = fields.Integer(string='Buts', required=True)
    total_rating = fields.Float(string='Note Totale', compute='_compute_total_rating')
    feedback = fields.Text(string='Commentaires')

    @api.depends('speed', 'dribbling', 'matches_played', 'goals')
    def _compute_total_rating(self):
        for evaluation in self:
            # Calculate the total rating as an average of the criteria
            evaluation.total_rating = (evaluation.speed + evaluation.dribbling + 
                                       evaluation.matches_played + evaluation.goals) / 4
