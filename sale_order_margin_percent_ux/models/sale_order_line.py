from odoo import models, fields, api, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # _compute_margin lo hago SOLO en el módulo en clima
    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        super(SaleOrderLine,self)._compute_margin()
        for line in self:
            costo_total = line.price_subtotal - line.margin
            line.margin_percent = costo_total and line.margin/costo_total
