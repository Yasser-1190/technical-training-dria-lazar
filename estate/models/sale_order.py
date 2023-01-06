from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('partner_id', 'amount_total')
    def check_max_sale_order_amount(self):
        for order in self:
            if order.partner_id.max_sale_order_amount and order.amount_total > order.partner_id.max_sale_order_amount:
                raise ValidationError(_('The sale order amount is greater than the maximum allowed amount for the partner.'))

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
