from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class KickappReservation(models.Model):
    _name = 'kickapp.reservation'
    _description = 'Réservation en Ligne'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    terrain_id = fields.Many2one('kickapp.terrain', string='Terrain', required=True)
    date = fields.Date(string='Date', required=True)
    heure_debut = fields.Datetime(string='Heure de Début', required=True)
    duree = fields.Float(string='Durée (en heures)', required=True)
    joueur_id = fields.Many2one('kickapp.joueur', string='Joueur')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')

    activity_calendar_event_id = fields.Many2one('calendar.event', string='Calendar Event')
    user_id = fields.Many2one('res.users', string='Utilisateur', required=True, default=lambda self: self.env.user)


    def unlink(self):
        for reservation in self:
            if reservation.activity_calendar_event_id:
                reservation.activity_calendar_event_id.unlink()
        return super(KickappReservation, self).unlink()

    def create_calendar_event(self):
        for reservation in self.filtered(lambda r: r.state == 'confirmed'):
            start_datetime_obj = fields.Datetime.from_string(reservation.heure_debut)
            if start_datetime_obj:
                stop_datetime_obj = start_datetime_obj + timedelta(hours=reservation.duree)
                event_values = {
                    'name': 'Reservation pour Terrain {}'.format(reservation.terrain_id.name),
                    'start': start_datetime_obj,
                    'stop': stop_datetime_obj,
                }
                event = self.env['calendar.event'].create(event_values)
                reservation.activity_calendar_event_id = event

    @api.model
    def create(self, vals):
        if 'date' in vals and 'terrain_id' in vals:
            existing_reservation = self.env['kickapp.reservation'].search([
                ('date', '=', vals['date']),
                ('terrain_id', '=', vals['terrain_id']),
                ('state', '!=', 'cancel')
            ])
            if existing_reservation:
                raise ValidationError("Le terrain choisi pour cette date est déjà réservé.")
        reservation = super(KickappReservation, self).create(vals)
        return reservation            

    def action_confirm_reservation(self):
        for reservation in self:
            reservation.state = 'confirmed'
            reservation.create_calendar_event()

    def action_draft_reservation(self):
        for reservation in self:
            reservation.state = 'draft'
            if reservation.activity_calendar_event_id:
                reservation.activity_calendar_event_id.unlink()

    def action_cancel_reservation(self):
        for reservation in self:
            reservation.state = 'cancel'
            if reservation.activity_calendar_event_id:
                reservation.activity_calendar_event_id.unlink()
        return super(KickappReservation, self).unlink()

    def action_done(self):
        for reservation in self:
            reservation.state = 'done'
            if reservation.activity_calendar_event_id:
                reservation.activity_calendar_event_id.unlink()

    @api.model
    def get_reservation_status_dates(self, terrain_id):
        today = fields.Date.today()
        reservations = self.search([
            ('terrain_id', '=', terrain_id),
            ('date', '>=', today),
        ])
        confirmed_dates = reservations.filtered(lambda r: r.state == 'confirmed').mapped('date')
        done_dates = reservations.filtered(lambda r: r.state == 'done').mapped('date')
        
        return {
            'confirmed_dates': confirmed_dates,
            'done_dates': done_dates,
        }
