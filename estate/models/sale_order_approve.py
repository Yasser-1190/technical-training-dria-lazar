from odoo import api, models, fields
from odoo.exceptions import ValidationError

class SaleOrderApprove(models.Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.approval'
    _description = 'Sale Order Approval'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        required=True,
        ondelete='cascade',
    )
    amount = fields.Float(
        string='Amount',
        required=True,
    )
    level = fields.Selection(
        string='Level',
        selection=[
            ('1', 'Level 1'),
            ('2', 'Level 2'),
            ('3', 'Level 3'),
            # add more levels as needed
        ],
        required=True,
        default='1',
    )
