# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrderMassActionWizard(models.TransientModel):

    _name = "sale.order.mass.action.wizard"
    _description = "Sale Order Mass Action"

    @api.model
    def _get_rem_product_id_domain(self):
        # order_line_product_ids = self.env.context.get("active_ids")
        if self.env.context.get("active_ids") and len(self.env.context.get("active_ids")) == 1:
            # import pdb; pdb.set_trace()
            return [("id", "in", self.env["sale.order.mpe.product.src"].search([]).mapped("src_product_id").ids),("id", "in",self.env["sale.order"].browse(self.env.context.get("active_ids")).order_line.mapped("product_id").ids)]
        else:
            return [("id", "in", self.env["sale.order.mpe.product.src"].search([]).mapped("src_product_id").ids)]

    rem_product_id = fields.Many2one('product.product', string='Quitar producto',domain=_get_rem_product_id_domain)

    add_product_id = fields.Many2one('product.product', string='Agregar producto')

    dest_product_ids = fields.One2many("product.product", compute="_compute_dest_product_ids")

    def _get_sale_order_confirm_domain(self):
        return [
            ("id", "in", self.env.context.get("active_ids")),
            ("state", "in", ("sale", "done")),
        ]

    def apply_button(self):
        sale_order_obj = self.env["sale.order"]
        if self.env.context.get("active_model") != "sale.order":
            return
        mass_product_exchange = self.env["sale.order.mass.product.exchange"]
        for wizard in self:
            vals = {
                'rem_product_id': wizard.rem_product_id.id,
                'add_product_id': wizard.add_product_id.id,
                'user_id': self.env.uid,
            }
            new_mpe = mass_product_exchange.create(vals)

            sale_orders = sale_order_obj.search(wizard._get_sale_order_confirm_domain())
            sale_orders.product_exchange(new_mpe,wizard.rem_product_id, wizard.add_product_id)
            # sale_orders.action_confirm()
            # self._notify_success(sale_orders)
        return True

    @api.depends('rem_product_id')
    def _compute_dest_product_ids(self):        
        if self.rem_product_id:
            self.dest_product_ids = self.env["sale.order.mpe.product.src"].search([("src_product_id","=",self.rem_product_id.id)])[0].dest_product_ids.mapped("dest_product_id")
        else:
            self.dest_product_ids = False