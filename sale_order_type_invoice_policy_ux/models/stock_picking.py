##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models, _
from odoo.tools import float_compare
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # src/addons-adhoc/sale/sale_order_type_invoice_policy/models/stock_picking.py:44
    def _check_sale_paid(self):
        
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')

        # que no tenga en cuenta las NC ni las facturas canceladas
        invoice_status = []
        for invoice in self.sale_id.invoice_ids.filtered(lambda x: x.move_type == 'out_invoice'):
            invoice_status.append(invoice.state)

        if (set(invoice_status) - set(['paid','cancel'])) or any(
                (float_compare(line.product_uom_qty,
                               line.qty_invoiced,
                               precision_digits=precision) > 0)
                for line in self.sale_id.order_line):
            return False
        return True
