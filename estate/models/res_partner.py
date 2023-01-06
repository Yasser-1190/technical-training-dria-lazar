from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    max_sale_order_amount = fields.Float(string='Maximum Sale Order Amount')