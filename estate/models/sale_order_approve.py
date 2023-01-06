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
        selection=[
            ('1', 'Level 1'),
            ('2', 'Level 2'),
            ('3', 'Level 3'),
            # add more levels as needed
        ],
        required=True,
        default='1',
    )
    
    def transition_approve(self):
        if self.amount < 500:
            return True
        return False
    
    def create_workflow(self):
        workflow = Workflow(self._name)
        # define the states
        workflow.add_state('pending_level_1_approval', 'Pending Level 1 Approval')
        workflow.add_state('pending_level_2_approval', 'Pending Level 2 Approval')
        workflow.add_state('approved', 'Approved')
        # define the transitions
        workflow.add_transition('approve', 'pending_level_1_approval', 'approved', condition=transition_approve)
        workflow.add_transition('reject', 'pending_level_1_approval', 'rejected')
        workflow.add_transition('escalate', 'pending_level_1_approval', 'pending_level_2_approval')
        # add more transitions as needed
        return workflow
