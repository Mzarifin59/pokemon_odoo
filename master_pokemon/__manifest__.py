{
    'name': 'Pokemon Master',
    'version': '1.0',
    'summary': 'Pokemon for company',
    'category': 'Extra Tools',
    'depends': ['base', 'contacts'],
    'data': [
        'security/pokemon_security.xml',
        'security/ir.model.access.csv',
        'data/res_group.xml',
        'views/pokemon_view.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}