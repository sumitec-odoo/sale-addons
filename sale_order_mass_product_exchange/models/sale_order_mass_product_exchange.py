# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderMassProductExchange(models.Model):
    _name = 'sale.order.mass.product.exchange'
    _order = 'id desc'
    _description = 'Cambio masivo de producto'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "rem_product_id"

    date = fields.Date('Fecha',default=fields.Datetime.now)

    user_id = fields.Many2one(
        'res.users', string='Realizado por',
        required=True,
        readonly=True)

    rem_product_id = fields.Many2one('product.product', string='Producto quitado')

    add_product_id = fields.Many2one('product.product', string='Producto agregado')

    mass_product_exchange_line_ids = fields.One2many('sale.order.mass.product.exchange.line', 'mass_product_exchange_id', string='Pedidos modificados')

    def facturar_action(self):
        # import pdb; pdb.set_trace()

        wiz = self.env['sale.advance.payment.inv'].with_context(active_ids=self.mass_product_exchange_line_ids.mapped("sale_order_id").ids, open_invoices=True).create({})

        return wiz.create_invoices()