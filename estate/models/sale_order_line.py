from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Char(string="Training Date")
    employee = fields.Char(string="Assigned Employee")
