from odoo import api, fields, models

class kickappTournament(models.Model):
    _name = 'kickapp.tournament'
    _description = 'Tournoi de Football'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom', required=True)
    start_date = fields.Date(string='Date de Début')
    end_date = fields.Date(string='Date de Fin')
    club_ids = fields.Many2many('kickapp.club', string='Clubs Participants')
    match_ids = fields.One2many('kickapp.match', 'tournament_id', string='Matchs')
    stadium_id = fields.Many2one('kickapp.terrain', string='Stade')

    @api.model
    def create(self, vals):
        record = super(kickappTournament, self).create(vals)
        event_vals = {
            'name': f"Tournoi: {record.name}",
            'date_begin': record.start_date,
            'date_end': record.end_date,
        }
        self.env['event.event'].create(event_vals)
        return record
