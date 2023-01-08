from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.datetime(year=2023, month=1, day= 1)
    employee = fields.Char(string="Assigned Employee")
    approval_status = fields.Selection(
    related='approval_id.state',
    string='Approval Status',
    )
