from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.datetime(auto_now_add=True, string="Training Date", year=2023)
    employee = fields.Char(string="Assigned Employee")
    approval_status = fields.Selection(
    related='approval_id.state',
    string='Approval Status',
    )
