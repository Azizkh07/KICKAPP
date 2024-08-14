from odoo import http
from odoo.http import request
import logging
import pytz
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class ReservationController(http.Controller):

    @http.route('/create_reservation', type='http', auth="user", methods=['POST'], website=True)
    def create_reservation(self, **post):
        try:
            terrain_id = post.get('terrain_id')
            if not terrain_id:
                raise ValueError("Il manque l'ID du terrain.")
            terrain_id = int(terrain_id)

            date = post.get('date')
            if not date:
                raise ValueError("Il manque la date.")
            date = datetime.strptime(date, '%Y-%m-%d')

            heure_debut = post.get('heure_debut')
            if not heure_debut:
                raise ValueError("Il manque l'heure de début.")
            heure_debut = datetime.strptime(heure_debut, '%H:%M').time()
            start_datetime = datetime.combine(date, heure_debut)

            user_tz = request.env.user.tz or 'UTC'
            local_tz = pytz.timezone(user_tz)
            local_datetime = local_tz.localize(start_datetime, is_dst=None)
            utc_datetime = local_datetime.astimezone(pytz.utc)

            # Make the datetime naive by removing the timezone information
            naive_utc_datetime = utc_datetime.replace(tzinfo=None)

            duree = post.get('duree')
            if not duree:
                raise ValueError("Il manque la durée.")
            duree = float(duree)
            if duree <= 0:
                raise ValueError("La durée doit être un nombre positif.")

            end_datetime = naive_utc_datetime + timedelta(hours=duree)

            existing_reservations = request.env['kickapp.reservation'].search([
                ('terrain_id', '=', terrain_id),
                ('heure_debut', '<', end_datetime),
                ('heure_debut', '>=', naive_utc_datetime)
            ])

            if existing_reservations:
                raise ValueError("Le créneau horaire sélectionné est déjà réservé.")

            request.env['kickapp.reservation'].create({
                'terrain_id': terrain_id,
                'date': date,
                'heure_debut': naive_utc_datetime,
                'duree': duree,
                'user_id': request.env.user.id,
            })

            return request.render("KICKAPP.template_success", {})

        except (ValueError, TypeError) as e:
            _logger.error(f"Erreur lors de la création de la réservation : {e}")
            return request.render("KICKAPP.template_success", {})

    @http.route('/reservation', type='http', auth="user", website=True)
    def reservation_form(self, **kwargs):
        terrains = request.env['kickapp.terrain'].search([])
        return request.render("KICKAPP.kickapp_reservation_template", {
            'terrains': terrains,
        })

    @http.route('/get_available_dates', type='json', auth='public', methods=['POST'])
    def get_available_dates(self, terrain_id):
        _logger.info(f"Received terrain_id: {terrain_id}")  # Log received data
        try:
            # Fetch reservations based on terrain_id
            reservations = request.env['kickapp.reservation'].search([
                ('terrain_id', '=', int(terrain_id)),
                ('state', '!=', 'cancel')
            ])
            event_data = []
            for reservation in reservations:
                start = reservation.heure_debut
                end = start + timedelta(hours=reservation.duree)
                event_data.append({
                    'title': 'Réservé',
                    'start': start.isoformat(),
                    'end': end.isoformat(),
                    'state': reservation.state
                })
            _logger.info(f"Returning event data: {event_data}")
            return event_data
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des dates disponibles : {e}")
            return {
                'code': 500,
                'message': 'Erreur du serveur Odoo',
                'data': str(e)
            }
