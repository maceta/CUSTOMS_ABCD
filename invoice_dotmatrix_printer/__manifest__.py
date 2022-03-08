# -*- coding: utf-8 -*-

{
    'name': 'Account Invoice Dotmatrix Printer',
    'version': '1.0',
    'category': 'Sale',
    'sequence': 6,
    'author': 'ErpMstar Solutions',
    'summary': 'Allows you to print Account Invoice report by dot matrix printer.',
    'description': "Allows you to print Account Invoice report by dot matrix printer.",
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/receipt.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 30,
    'currency': 'EUR',
}
