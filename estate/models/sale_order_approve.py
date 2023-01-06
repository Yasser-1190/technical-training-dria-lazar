from odoo import api, models, fields
from odoo.exceptions import ValidationError

class SaleOrderApprove(models.Model):
    _name = 'sale.order.approval'
    _inherit = 'sale.order.line'
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
        # level selection
        selection=[
            ('1', 'Level 1'),
            ('2', 'Level 2'),
            ('3', 'Level 3'),
        ],
        required=True,
        default='1',
    )
    
    def create_workflow(self):
        workflow = Workflow(self._name)
        # states
        workflow.add_state('pending_level_1_approval', 'Pending Level 1 Approval')
        workflow.add_state('pending_level_2_approval', 'Pending Level 2 Approval')
        workflow.add_state('approved', 'Approved')

        def transition_approve(self, cr, uid, ids, context=None):
            for approval in self.browse(cr, uid, ids, context=context):
                if approval.amount < 500:
                    return True
            return False

        # transitions
        workflow.add_transition('approve', 'pending_level_1_approval', 'approved', condition=transition_approve)
        workflow.add_transition('reject', 'pending_level_1_approval', 'rejected')
        workflow.add_transition('escalate', 'pending_level_1_approval', 'pending_level_2_approval')
        return workflow

    @api.one
    def check_amount(self):
        for order in self:
            if order.amount < 500:
                order.approval_id.approve()
            elif 500 <= order.amount < 2000:
                order.approval_id.escalate()
            elif 2000 <= order.amount < 5000:
                order.approval_id.escalate()