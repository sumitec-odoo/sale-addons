# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    volume = fields.Float(compute='_compute_volume', string='Volumen total', readonly=True, store=True)

    @api.depends('order_line.product_uom_qty')
    def _compute_volume(self):
        for order in self:
            volume = qty = 0.0
            # filtro los que no son productos (secciones / notas)
            for line in order.order_line.filtered(lambda x: not x.display_type):
                qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
                volume += (line.product_id.volume or 0.0) * qty
            order.update({
                'volume': volume,
            })