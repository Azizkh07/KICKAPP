from odoo import fields, models,api


class ResPartner(models.Model):
    """Inherit res partner"""
    _inherit = 'res.partner'
    membre = fields.Boolean(string='Membre Kickapp', default=True)
    is_coach = fields.Boolean(string='Est Entraîneur')
    is_joueur = fields.Boolean(string='Est Joueur')
    is_abonne_club = fields.Boolean(string='Est Abonné du Club')
    is_recruiter = fields.Boolean(string="Recruteur")
    
    club_subscription_ids = fields.One2many('kickapp.club.subscription', 'partner_id', string='Club Subscriptions')

    
    club_subscription_count = fields.Integer(
        string='Club Subscription Count',
        compute='_compute_club_subscription_count',
        help='Number of club subscriptions for this partner'
    )

    @api.depends('club_subscription_ids')
    def _compute_club_subscription_count(self):
        for partner in self:
            partner.club_subscription_count = self.env['kickapp.club.subscription'].search_count([
                ('partner_id', '=', partner.id)
            ])
 