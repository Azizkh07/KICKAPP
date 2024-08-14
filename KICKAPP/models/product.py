from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    Prod = fields.Boolean(string='Produit Kickapp',
                                 help='This help to define the product whether'
                                      'it is kickapp product')
    
