# -*- coding: utf-8 -*-

{
    'name': 'Xion Technologies',
    'version': '1.1.0',
    'category': 'Technology',
    'license': '',
    'summary': 'APP centralizadora de clientes, tratamientos y suscripciones',
    'description': """
APP desarrollada por Xion Technologies que permite gestionar clientes, suscripciones, tratamientos, sesiones y productos.
    """,
    'author': 'Omar Rodrigo Ruelas Príncipe',
    'depends': [
        'base',
        'membership',
    ],
    'data': [
        'views/res_xion_views.xml', # Settings
        'views/inherit_xion_views.xml', # Inherited
        'views/xion_views.xml', # Operations
        'views/menu_xion_views.xml', # Menus
        'security/ir.model.access.csv' # Access
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
