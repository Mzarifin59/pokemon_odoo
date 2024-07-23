{
    'name': 'Inventory ABC Retail Custom',
    'version': '1.0',
    'summary': 'Custom Fields For Inventory Module',
    'description': 'Sebuah custom modul untuk menambah atau mengubah field produk pada inventory produk',
    'author': 'Rifky Arifin',
    'website': '',
    'category': 'Inventory',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
    'installable': True,
    'application': True,
}