##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models, _
# from odoo.tools import float_compare
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # addons-adhoc/sale/sale_order_type_invoice_policy/models/stock_picking.py:42
    def _check_sale_paid(self):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        invoice_status = self.sale_id.mapped(
            'order_line.invoice_lines.move_id').filtered(lambda x: x.move_type == 'out_invoice' and x.state != 'cancel').mapped('payment_state')
        if (set(invoice_status) - set(['paid', 'in_payment'])) or any(
                not float_is_zero(line.qty_to_invoice, precision_digits=precision)
                for line in self.sale_id.order_line):
            return False
        return True