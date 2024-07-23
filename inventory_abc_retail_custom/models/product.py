from odoo import models, fields

class FieldsProduct(models.Model):
    _inherit = 'product.template'

    bahan = fields.Char('Material')
    warna = fields.Char('Color')
    ukuran = fields.Char('Size')
    ketersediaan = fields.Selection([
        ('tersedia', 'Avaible'),
        ('tidak_tersedia', 'Unavailable')                                                 
    ], string='Availability Status')
    kadaluwarsa = fields.Date('Expired Date')
    lokasi_penyimpanan = fields.Char('Inventory Location')
    intruksi_perawatan = fields.Text('Care Instructions')
    kondisi_produk = fields.Selection([
        ('bagus', 'Good'),
        ('kurang_bagus', 'Not Good'),
        ('rusak', 'Damaged')
    ], string='Product Condition')
    