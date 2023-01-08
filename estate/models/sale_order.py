from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def check_max_sale_order_amount(self):
        for order in self:
            if order.partner_id.max_sale_order_amount and order.amount_total > order.partner_id.max_sale_order_amount:
                raise ValidationError(_('The sale order amount is greater than the maximum allowed amount for the partner.'))

    approval_status = fields.Selection(
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
    
    def action_confirm(self):
        # Confirm the sales order
        res = super(SaleOrder, self).action_confirm()

        # Create the event and send the email
        event = self.env['calendar.event'].create({
            'name': self.name,
            'start_date': self.date_order,
            'end_date': self.date_order,
            'description': self.note,
            'location': self.partner_shipping_id.name,
            'attendee_ids': [(6, 0, [self.user_id.partner_id.id])],
            'organizer_id': self.user_id.partner_id.id,
            'privacy': 'private'
        })
        template = self.env.ref('my_module.email_template_sale_order_confirm')
        template.send_mail(event.id, force_send=True)

        return res
