from odoo import models, fields, api
from odoo.exceptions import ValidationError

class kickappJoueur(models.Model):
    _name = 'kickapp.joueur'
    _description = 'Profil du Joueur'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Pour les notifications par mail

    name = fields.Char(string='Nom du Joueur', required=True)
    age = fields.Integer(string="Age")
    email = fields.Char(string='Email')
    telephone = fields.Char(string='Téléphone')
    club_id = fields.Many2one("kickapp.club", "Club")
    poste = fields.Selection([
        ("gauche", "Gauche"),
        ("droite", "Droite"),
        ("milieu", "Milieu"),
        ("gardien", "Gardien"),
        ("attaquant", "Attaquant"),
        ("défenseur", "Défenseur"),
    ], string='Poste', help='Poste de joueur')
    image = fields.Binary(string='Image du Joueur')
    is_talent = fields.Boolean(string='Est un Talent', compute='_compute_is_talent')
    average_rating = fields.Float(string='Note Moyenne', compute='_compute_average_rating')
    
    @api.constrains('telephone')
    def _check_telephone_length(self):
        for joueur in self:
            if joueur.telephone and len(joueur.telephone) != 8:
                raise ValidationError("Le numéro de téléphone doit contenir exactement 8 chiffres !")
    
    def create_contact(self):
        for joueur in self:
            # Create contact values
            contact_values = {
                'name': joueur.name,
                'image_1920': joueur.image,
                'is_joueur': True,
                # Add other fields as needed
            }
            # Create contact
            self.env['res.partner'].create(contact_values)

    @api.model
    def create(self, vals):
        joueur = super(kickappJoueur, self).create(vals)
        joueur.create_contact()
        return joueur
    
    @api.model
    def get_joueurs_count(self):
        joueurs_count = self.env['kickapp.joueur'].search_count([])
        return joueurs_count
    
    @api.depends('evaluation_ids')
    def _compute_is_talent(self):
        for joueur in self:
            evaluations = joueur.evaluation_ids.filtered(lambda e: e.coach_id)
            if evaluations:
                # Calculate average ratings for the specified criteria
                total_speed = sum(evaluation.speed for evaluation in evaluations)
                total_dribbling = sum(evaluation.dribbling for evaluation in evaluations)
                total_matches_played = sum(evaluation.matches_played for evaluation in evaluations)
                total_goals = sum(evaluation.goals for evaluation in evaluations)
                count = len(evaluations)
                # Define your threshold for being considered a talent
                if (total_speed / count > 7 and total_dribbling / count > 7 and
                        total_matches_played / count > 7 and total_goals / count > 7):
                    joueur.is_talent = True
                else:
                    joueur.is_talent = False
            else:
                joueur.is_talent = False

    @api.depends('evaluation_ids')
    def _compute_average_rating(self):
        for joueur in self:
            evaluations = joueur.evaluation_ids.filtered(lambda e: e.coach_id)
            if evaluations:
                joueur.average_rating = sum(
                    evaluation.total_rating for evaluation in evaluations
                ) / len(evaluations)
            else:
                joueur.average_rating = 0

    evaluation_ids = fields.One2many('kickapp.evaluation', 'player_id', string='Évaluations')
