from odoo import models, fields

class ClubEvent(models.Model):
    _name = 'kickapp.club.event'
    _description = 'Club Event'
    _inherit=['mail.thread','mail.activity.mixin'] # Pour les notifications par mail

    name = fields.Char(string='Event Name', required=True)
    event_type = fields.Selection([('training', 'Training'), ('match', 'Match')], string='Event Type', required=True)
    start_datetime = fields.Datetime(string='Start Date and Time', required=True)
    end_datetime = fields.Datetime(string='End Date and Time', required=True)
    club_id = fields.Many2one('kickapp.club', string='Club', required=True)
    coach_id = fields.Many2one('kickapp.coach', string='Coach')
    state = fields.Selection([('new', 'New'), ('read', 'Read')], string='Event State', default='new')
    
    def mark_as_read(self):
        self.write({'state': 'read'})





    