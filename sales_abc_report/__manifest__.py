{
    'name': 'Sales ABC Retail Custom',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom reports for most sold items and expiring items',
    'depends': ['sale', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'reports/most_sold_items_report.xml',
        'reports/expiring_items_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}