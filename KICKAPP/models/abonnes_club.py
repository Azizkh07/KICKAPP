from odoo import models, fields,api

class ClubSubscriber(models.Model):
    _name = 'kickapp.club.subscriber'
    _description = 'Club Subscriber'
    _inherit=['mail.thread','mail.activity.mixin'] # Pour les notifications par mail


    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    start_date = fields.Date(string='Start Date')
    expiration_date = fields.Date(string='Expiration Date')
    club_id = fields.Many2one('kickapp.club', string='Club')

    
    def create_contact(self):
        for club_subscriber in self:
            # Create contact values
            contact_values = {
                'name': club_subscriber.name,
                'is_abonne_club': True,  # Set the field for club subscribers
                # Add other fields as needed
            }

            # Create contact
            club_subscriber = self.env['res.partner'].create(contact_values)

    @api.model
    def create(self, vals):
        club_subscriber = super(ClubSubscriber, self).create(vals)
        club_subscriber.create_contact()
        return club_subscriber