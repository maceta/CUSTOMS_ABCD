# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': "Point of Sale (POS) with On Hand Quantity",
    'price': 19.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': """This module show product stock quantity on Point of Sales.""",
    'description': """
Show the Available Quantity On Point Of Sale Screen.
Quantity On Point Of Sale Screen.
Quantity On POS.
pos quantity
point of sale qty
point of sale quantity
pos product quantity
show product quantity
product quantity on point of sale
point of sale stock show
product stock show on point of sale
point of sale item quantity
Show Product Stock Quantity on Point of Sale
Check this box if you want to show qty on hand on POS for stockable product type.

pos_stock
POS Stock
Display Stock in POS interface
This module show product stock quantity (Quantity on hand) on Point of Sales.
Check this box if you want to show qty on hand on POS for stockable product type.
POS Stock Details


""",
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "www.probuse.com",
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.png'],
    'live_test_url': 'http://probuseappdemo.com/probuse_apps/pos_sale_item_info/627',#'https://youtu.be/Ji5zibaeCiM',
    'version': '2.2',
    'category' : 'Point Of Sale',
    'depends': ['point_of_sale'],
    'data':[
        'views/pos_templates.xml',
        'views/product_view.xml',
    ],
    'qweb' : [
        # 'static/src/xml/point_of_sale.xml', #odoo13
        'static/src/xml/ProductItem.xml' #odoo14
    ],
    'installable' : True,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
