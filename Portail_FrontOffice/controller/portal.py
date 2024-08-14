from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from datetime import datetime, timedelta
from odoo import http, fields, models, _
from odoo.http import request
from dateutil.relativedelta import relativedelta
import logging


class KickappPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        ret = super(KickappPortal, self)._prepare_home_portal_values(counters)
        # Remove the recruiter check to make the joueurs_count available for everyone
        ret["joueurs_count"] = request.env['kickapp.joueur'].search_count([])

        return ret

    @http.route(['/my/joueurs', '/my/joueurs/page/<int:page>'], type='http', website=True)
    def kickapp_joueurs_list_view(self, page=1, sortby='id', search="", search_in="All", **kw):
        # Remove the recruiter check to allow everyone to access the joueurs list
        sorted_list = {
            'id': {'label': 'ID Desc', 'order': 'id desc'},
            'name': {'label': 'Nom', 'order': 'name'},
        }
        search_list = {
            'All': {'label': 'Tous', 'input': 'all', 'domain': []},
            'name': {'label': 'Nom de joueur', 'input': 'name', 'domain': [('name', 'ilike', search)]},
        }

        search_domain = search_list[search_in]['domain']
        default_order_by = sorted_list[sortby]['order']
        joueurs_obj = request.env['kickapp.joueur']
        total_joueurs = joueurs_obj.search_count(search_domain)
        page_detail = request.website.pager(
            url='/my/joueurs', total=total_joueurs, page=page,
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search}, step=5
        )
        joueurs = joueurs_obj.search(search_domain, limit=5, order=default_order_by, offset=page_detail['offset'])
        vals = {
            'joueurs': joueurs,
            'page_name': 'Joueurs_list_view',
            'pager': page_detail,
            'sortby': sortby,
            'searchbar_sortings': sorted_list,
            'search_in': search_in,
            'searchbar_inputs': search_list,
            'search': search,
        }
        return request.render('Portail_FrontOffice.kickapp_joueurs_list_view_portal', vals)

    @http.route(['/my/joueur/<model("kickapp.joueur"):joueur_id>'], type='http', website=True)
    def kickapp_joueurs_form_view(self, joueur_id, **kw):
        # Remove the recruiter check to allow everyone to access the joueurs form view
        vals = {"joueur": joueur_id, 'page_name': 'Joueurs_form_view'}
        joueurs_records = request.env['kickapp.joueur'].search([])
        joueurs_ids = joueurs_records.ids
        joueurs_index = joueurs_ids.index(joueur_id.id)
        if joueurs_index != 0 and joueurs_ids[joueurs_index-1]:
            vals['prev_record'] = '/my/joueur/{}'.format(joueurs_ids[joueurs_index-1])
        if joueurs_index < len(joueurs_ids) - 1 and joueurs_ids[joueurs_index + 1]:
            vals['next_record'] = '/my/joueur/{}'.format(joueurs_ids[joueurs_index + 1])

        return request.render('Portail_FrontOffice.kickapp_joueurs_form_view_portal', vals)

    
    
    
    
    @http.route(['/my/recruit_talent'], type='http',website=True)
    def recruit_talent(self, joueur_id=None, **kwargs):
        
        if joueur_id:
            
            joueur = request.env['kickapp.joueur'].browse(int(joueur_id))
            
            if joueur:
                
                return request.render('Portail_FrontOffice.recruitment_page_template', {'joueur': joueur})
    
        return request.redirect('/my/joueurs')

    
    @http.route(['/my/submit_recruit_talent'], type='http', website=True)
    def submit_recruit_talent(self, **kwargs):
        joueur_name = kwargs.get('name')
        
        joueur_email = kwargs.get('email')
        joueur_telephone = kwargs.get('telephone')
        job_id = 2  # Remplacez par l'ID de votre poste spécifique
        

        if joueur_name and joueur_email and joueur_telephone:
            
            
            recruitment_process = request.env['hr.applicant'].sudo().create({
                
            'name': joueur_name,
            'partner_name': joueur_name,
            'email_from': joueur_email,
            'partner_phone': joueur_telephone,
            'job_id': job_id
        })
            return request.redirect('/my/recruitment_confirmation/%s' % recruitment_process.id)
    
        return request.redirect('/my/joueurs')
    
    
    @http.route(['/my/recruitment_confirmation/<int:recruitment_id>'], type='http', website=True)
    def recruitment_confirmation(self, recruitment_id, **kwargs):
        recruitment_process = request.env['hr.applicant'].sudo().browse(recruitment_id)
        if recruitment_process:
            return request.render('Portail_FrontOffice.recruitment_confirmation_template', {'recruitment_process': recruitment_process})
        
        return request.redirect('/my/joueurs')


_logger = logging.getLogger(__name__)
class KickappPortalclub(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        ret = super(KickappPortalclub, self)._prepare_home_portal_values(counters)
        ret["clubs_count"] = request.env['kickapp.club'].search_count([])
        return ret

    @http.route(['/my/clubs', '/my/clubs/page/<int:page>'], type='http', website=True)
    def kickapp_clubs_list_view(self, page=1, sortby='id', search="", search_in="All", **kw):
        sorted_list = {
            'id': {'label': 'ID Desc', 'order': 'id desc'},
            'name': {'label': 'Nom', 'order': 'name'},
        }
        search_list = {
            'All': {'label': 'Tous', 'input': 'all', 'domain': []},
            'name': {'label': 'Nom du club', 'input': 'name', 'domain': [('name', 'ilike', search)]},
        }
        search_domain = search_list[search_in]['domain']
        default_order_by = sorted_list[sortby]['order']
        clubs_obj = request.env['kickapp.club']
        total_clubs = clubs_obj.search_count(search_domain)
        page_detail = request.website.pager(
            url='/my/clubs', total=total_clubs, page=page,
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search}, step=5
        )
        clubs = clubs_obj.search(search_domain, limit=5, order=default_order_by, offset=page_detail['offset'])
        vals = {
            'clubs': clubs,
            'page_name': 'Clubs_list_view',
            'pager': page_detail,
            'sortby': sortby,
            'searchbar_sortings': sorted_list,
            'search_in': search_in,
            'searchbar_inputs': search_list,
            'search': search,
        }
        return request.render('Portail_FrontOffice.kickapp_clubs_list_view_portal', vals)

    @http.route(['/my/club/<model("kickapp.club"):club_id>'], type='http', website=True)
    def kickapp_clubs_form_view(self, club_id, **kw):
        vals = {"club": club_id, 'page_name': 'Clubs_form_view'}
        return request.render('Portail_FrontOffice.kickapp_club_form_view_portal', vals)

    @http.route(['/my/subscribe_club'], type='http', website=True)
    def subscribe_club(self, club_id=None, **kwargs):
        if club_id:
            club = request.env['kickapp.club'].browse(int(club_id))
            if club:
                return request.render('Portail_FrontOffice.subscription_page_template', {'club': club})
            return request.redirect('/my/clubs')

  
    @http.route(['/my/submit_subscribe_club'], type='http', website=True, csrf=True)
    def submit_subscribe_club(self, **kwargs):
        club_id = kwargs.get('club_id')
        user = request.env.user

        if not club_id:
            _logger.error("No club ID provided.")
            return request.redirect('/my/clubs')

        try:
            club = request.env['kickapp.club'].sudo().browse(int(club_id))
            if not club:
                _logger.error("Club with ID %s not found.", club_id)
                return request.redirect('/my/clubs')

            if not club.subscription_product_id:
                product_template = request.env['product.template'].sudo().create({
                    'name': f"Abonnement {club.name}",
                    'type': 'service',
                    'list_price': 100.00,
                })

                product = request.env['product.product'].sudo().search([
                    ('product_tmpl_id', '=', product_template.id)
                ], limit=1)

                if not product:
                    product = request.env['product.product'].sudo().create({
                        'product_tmpl_id': product_template.id,
                    })

                club.sudo().subscription_product_id = product.id
            else:
                product = club.subscription_product_id

            # Create or update the sale order
            sale_order = request.website.sale_get_order(force_create=1)
            sale_order._cart_update(
                product_id=product.id,
                add_qty=1,
                set_qty=1,
            )

            # Create the club subscription record
            subscription = request.env['kickapp.club.subscription'].sudo().create({
                'partner_id': user.partner_id.id,
                'club_id': club.id,
                'state': 'draft',  # State is set to draft initially
                'start_date': fields.Date.today(),
                'end_date': fields.Date.today() + relativedelta(years=1)
            })

            # Update is_abonne_club and subscription count
            user.partner_id.is_abonne_club = True
            user.partner_id._compute_club_subscription_count()

            _logger.info("Redirecting to the cart page for user ID %s.", user.id)
            return request.redirect('/shop/cart')

        except Exception as e:
            _logger.error("Error occurred while processing subscription for club ID %s: %s", club_id, str(e))
            return request.redirect('/my/clubs')





