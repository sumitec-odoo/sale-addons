# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def product_exchange(self, mass_product_exchange_id, rem_product_id, add_product_id, quantity):

        mass_product_exchange_line_id = self.env["sale.order.mass.product.exchange.line"]

        vals_mpel = {
            'mass_product_exchange_id': mass_product_exchange_id.id,
            'sale_order_id': 0,
        }
        for rec in self:
            # producto_cambiado = False
            order_line_rem_ids = rec.order_line.filtered(lambda x: x.product_id.id == rem_product_id.id and x.product_uom_qty > 0)
            total_qty = sum(order_line_rem_ids.mapped("product_uom_qty"))
            if quantity > total_qty:
                raise UserError("La cantidad que se desea cambiar ({}) supera a la cantidad pedida ({}) en {}".format(quantity,total_qty,rec.name))
                        
            order_line_add_ids = rec.order_line.filtered(lambda x: x.product_id.id == add_product_id.id)
            if not order_line_add_ids:
                # si no existe un renglón para el producto agregado, lo creo
                vals = {
                        "order_id": rec.id,
                        "name": add_product_id.name,
                        "product_id": add_product_id.id,
                        "product_uom_qty": quantity,
                        "product_uom": add_product_id.uom_id.id,
                        "price_unit": order_line_rem_ids[0].price_unit,
                        }

                order_line_add_ids = self.env["sale.order.line"].sudo().create(vals)
            else:
                # si existe, lo actualizo
                order_line_add_ids[0].product_uom_qty += quantity

            qty_to_exchange = quantity
            for line in order_line_rem_ids:
                price_unit = line.price_unit
                
                if qty_to_exchange > line.product_uom_qty: 
                    # tiene que continuar el bucle hasta que qty_to_exchanged = 0
                    # que no quede nada para intercambiar
                    qty_to_exchange = qty_to_exchange - line.product_uom_qty
                    line.product_uom_qty = 0
                else:
                    # cant a intercambiar es menor que la cant de la línea.
                    # no hay más que intercambiar. finaliza el bucle
                    line.product_uom_qty = line.product_uom_qty - qty_to_exchange
                    break

            vals_mpel["sale_order_id"] = rec.id

            mass_product_exchange_line_id.sudo().create(vals_mpel)

        return True
