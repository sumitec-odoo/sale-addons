from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.margin', 'amount_untaxed')
    def _compute_margin(self):
        super(SaleOrder,self)._compute_margin()
        for order in self:
            costo_total = order.amount_untaxed - order.margin
            order.margin_percent = costo_total and order.margin/costo_total

