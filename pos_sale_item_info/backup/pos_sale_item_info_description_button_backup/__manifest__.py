# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': "Pos Sale Item Info",
    'price': 0.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': """This module Show the Default code of Product on POS.""",
    'description': """
Show the default code of product on pos product screen and payment receipt""",
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "www.probuse.com",
    'support': 'contact@probuse.com',
#    'images': ['static/description/img1.jpg'],
    'version': '1.0',
    'category' : 'Point Of Sale',
    'depends': ['point_of_sale'],
    'data':[
        'views/pos_templates.xml',
    ],
    'qweb' : [
        'static/src/xml/pos.xml',
    ],
    'installable' : True,
    'application' : False,
    'auto_install' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
