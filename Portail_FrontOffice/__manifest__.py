{
    'name': "PORTAIL_KICKAPP",
    'version': '1.0',
    'depends': ['base','web','website','portal','KICKAPP','hr_recruitment','sale','account'],
    'author': 'Mohamed aziz khannoussi',
    'category': 'Sport',
    'description': "PORTAIL FRONTOFFICE KICKAPP",
    
    'data': [
        'views/portail.xml',
        'views/portail_club.xml',
        'views/subscription.xml',
        'views/subscription_confirm.xml', 
        'views/recrutement.xml',
        'views/recrutement_confirm.xml',
      
        
],
  
    

    
    'installable': True,
    'application': True,
    'auto_install': False,

}
