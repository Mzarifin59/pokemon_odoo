from odoo import models, fields, api, tools
from datetime import datetime, timedelta

class TopSellingReport(models.Model):
    _name = 'custom.most.sold.items.report'
    _description = 'Top Selling Products Report'
    _auto = False

    product_id = fields.Many2one('product.product', string='Product')
    product_qty = fields.Float(string='Quantity Sold')
    product_category = fields.Many2one('product.category', string='Category')
    sale_date = fields.Date(string='Sale Date')

    def _select(self):
        return """
            SELECT
                MIN(l.id) as id,
                l.product_id as product_id,
                SUM(l.product_uom_qty) as product_qty,
                pt.categ_id as product_category,
                s.date_order::date as sale_date
            """

    def _from(self):
        return """
            FROM sale_order_line l
            JOIN sale_order s ON l.order_id = s.id
            JOIN product_product p ON l.product_id = p.id
            JOIN product_template pt ON p.product_tmpl_id = pt.id
            """

    def _group_by(self):
        return """
            GROUP BY
                l.product_id,
                pt.categ_id,
                s.date_order::date
            """

    @api.model
    def _get_report_values(self, docids, data=None):
        self.env.cr.execute(f'{self._select()} {self._from()} {self._group_by()}')
        result = self.env.cr.fetchall()
        return {
            'doc_ids': docids,
            'doc_model': 'sale.report',
            'data': data,
            'docs': result,
        }

    @api.model
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(f"""
            CREATE or REPLACE VIEW {self._table} as (
                {self._select()}
                {self._from()}
                {self._group_by()}
            )
        """)

class ProductExpiryReport(models.Model):
    _inherit = 'product.template'

    expiring_7_days = fields.Boolean(compute='_compute_expiry', store=True, string='Expiring in 7 Days')
    expiring_1_month = fields.Boolean(compute='_compute_expiry', store=True, string='Expiring in 1 Month')
    expiring_1_year = fields.Boolean(compute='_compute_expiry', store=True, string='Expiring in 1 Year')

    @api.model
    def get_product_expiry_data(self):
        products = self.search([])
        report_data = []
        for product in products:
            report_data.append({
                'name': product.name,
                'expiry_date': product.kadaluwarsa,
                'category': product.categ_id.name,
            })
        return report_data 

    @api.depends('kadaluwarsa')
    def _compute_expiry(self):
        today = fields.Date.today()
        for product in self:
            if product.kadaluwarsa:
                product.expiring_7_days = today <= product.kadaluwarsa <= today + timedelta(days=7)
                product.expiring_1_month = today <= product.kadaluwarsa <= today + timedelta(days=30)
                product.expiring_1_year = today <= product.kadaluwarsa <= today + timedelta(days=365)
            else:
                product.expiring_7_days = False
                product.expiring_1_month = False
                product.expiring_1_year = False