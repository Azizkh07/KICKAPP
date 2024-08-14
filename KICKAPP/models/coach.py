from odoo import models, fields, api
from odoo.exceptions import UserError

class KickappCoach(models.Model):
    _name = 'kickapp.coach'
    _description = 'Entraîneur de Football'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom de l\'Entraîneur', required=True)
    club_ids = fields.Many2many('kickapp.club', string='Clubs Entraînés')
    evaluation_ids = fields.One2many('kickapp.evaluation', 'coach_id', string='Évaluations des Joueurs')
    image = fields.Binary(string='Image du Coach')
    user_id = fields.Many2one('res.users', string='Utilisateur Interne', readonly=True)

    def create_event(self, event_data):
        event_data['coach_id'] = self.id
        event = self.env['kickapp.club.event'].create(event_data)

        # Notifier le club associé à cet événement
        event.club_id.has_unread_events = True

        return event

    def create_contact(self):
        for coach in self:
            # Create contact values
            contact_values = {
                'name': coach.name,
                'image_1920': coach.image,
                'is_coach': True,
                # Add other fields as needed
            }

            # Create contact
            self.env['res.partner'].create(contact_values)

    @api.model
    def create(self, vals):
        coach = super(KickappCoach, self).create(vals)
        coach.create_contact()
        return coach

    def create_internal_user(self):
        for coach in self:
            if coach.user_id:
                raise UserError("L'utilisateur interne pour cet entraîneur existe déjà.")

            # Créer l'utilisateur interne
            user_vals = {
                'name': coach.name,
                'login': f"{coach.name.lower().replace(' ', '_')}@kickapp.com",
                'partner_id': self.env['res.partner'].search([('name', '=', coach.name)], limit=1).id,
                'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],  # Utilisateur interne (groupe utilisateur)
            }
            user = self.env['res.users'].create(user_vals)
            coach.user_id = user.id
