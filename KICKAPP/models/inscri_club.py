from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ClubSubscription(models.Model):
    _name = 'kickapp.club.subscription'
    _description = 'Club Subscription'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    club_id = fields.Many2one('kickapp.club', string='Club', required=True)
    state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid'), ('expired', 'Expired')], string='State', default='draft')
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date', default=lambda self: fields.Date.today() + relativedelta(years=1))

    @api.model
    def create(self, vals):
        res = super(ClubSubscription, self).create(vals)
        if res:
            res._update_club_subscribers_count()
        return res

    def action_set_paid(self):
        for record in self:
            record.state = 'paid'
            record._update_club_subscribers_count()

    @api.model
    def _update_club_subscribers_count(self):
        for subscription in self:
            if subscription.club_id:
                subscription.club_id._compute_subscribers_count()
