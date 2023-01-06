from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_status = fields.Selection(
    related='approval_id.state',
    string='Approval Status',
    )

    approval_id = fields.Many2one(
        'sale.order.approval',
        string='Approval',
        ondelete='cascade',
    )

    def initiate_approval(self):
        self.ensure_one()
        approval = self.env['sale.order.approval'].create({
            'sale_order_id': self.id,
            'amount': self.amount,
            'level': '1',
        })
        approval.approve()
