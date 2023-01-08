from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.datetime(year=2023, month=1, day= 1)
    employee = fields.Many2one(string="Assigned Employee")
