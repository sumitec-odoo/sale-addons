# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def product_exchange(self, mass_product_exchange_id, rem_product_id, add_product_id):

        mass_product_exchange_line_id = self.env["sale.order.mass.product.exchange.line"]

        vals_mpel = {
            'mass_product_exchange_id': mass_product_exchange_id.id,
            'sale_order_id': 0,
        }
        for rec in self:

            for line in rec.order_line.filtered(lambda x: x.product_id.id == rem_product_id.id):
                product_qty = line.product_uom_qty
                price_unit = line.price_unit
                
                line.product_uom_qty = 0

                vals = {
                        "order_id": rec.id,
                        "name": add_product_id.name,
                        "product_id": add_product_id.id,
                        "product_uom_qty": product_qty,
                        "product_uom": add_product_id.uom_id.id,
                        "price_unit": price_unit,
                        }

                self.env["sale.order.line"].create(vals)

            vals_mpel["sale_order_id"] = rec.id

            mass_product_exchange_line_id.create(vals_mpel)

        return
