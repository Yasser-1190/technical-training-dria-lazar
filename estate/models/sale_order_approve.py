from odoo import api, models, fields
from odoo.exceptions import ValidationError

class SaleOrderApprove(models.Model):
    _inherit = 'sale.order.line'
    
