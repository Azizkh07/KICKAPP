from odoo import api, fields, models

class kickappMatch(models.Model):
    _name = 'kickapp.match'
    _description = 'Match de Football'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    tournament_id = fields.Many2one('kickapp.tournament', string='Tournoi')
    date = fields.Date(string='Date', required=True)
    home_team_id = fields.Many2one('kickapp.club', string='Équipe Domicile')
    away_team_id = fields.Many2one('kickapp.club', string='Équipe Visiteur')
    stadium_id = fields.Many2one('kickapp.terrain', string='Stade')

    @api.model
    def create(self, vals):
        record = super(kickappMatch, self).create(vals)
        event_vals = {
            'name': f"Match: {record.home_team_id.name} vs {record.away_team_id.name}",
            'date_begin': record.date,
            'date_end': record.date,
        }
        self.env['event.event'].create(event_vals)
        return record
