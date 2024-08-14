{
    'name': "kick_app",
    'version': '1.0',
    'depends': ['base','hr','calendar','contacts','sale','web','website','purchase','board','account','membership',
                'stock','hr_recruitment','event','point_of_sale'],
    'author': 'Mohamed aziz khannoussi',
    'category': 'Sport',
    'description': """
        Module Odoo pour la gestion de terrains de football, réservation en ligne, et recrutement de nouveaux talents.
    """,
    'data': [
      
        
        'security/ir.model.access.csv',
        'views/terrain.xml',
        'views/club.xml',
        'views/coach.xml',
        'views/evaluation.xml',
        'views/joueurs.xml',
        'views/reservation.xml',
        'views/match.xml',
        'views/tournoi.xml',
        'views/abonnes_club.xml',
        'views/calendrier_club.xml',
        'views/cassier.xml',
        'views/manager.xml',
        'views/menu.xml',
        'views/res_partner_views.xml',
        'views/product.xml',
        'views/inscri_club.xml',
        'views/kickapp_reservation_view.xml',
        'views/template.xml',
        'views/reservation_menu.xml',
        'security/security.xml',
    
      
       
],
    
'assets': {
        'web.assets_frontend':
            [
            'KICKAPP/static/src/js/custom_reservation.js',
            'KICKAPP/static/src/css/custom_reservation.css',
            ],
        },
   'qweb': [],

    
    'installable': True,
    'application': True,
    'auto_install': False,

}

