# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderMassProductExchangeLine(models.Model):
    _name = 'sale.order.mass.product.exchange.line'
    _order = 'id desc'
    # _description = 'Cambio masivo de producto'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = "rem_product_id"

    mass_product_exchange_id = fields.Many2one('sale.order.mass.product.exchange', string='Cambio masivo de producto')

    sale_order_id = fields.Many2one('sale.order', string='Pedido')

    sale_order_partner_id = fields.Many2one(related="sale_order_id.partner_id", string="Cliente")

    sale_order_state = fields.Selection(related="sale_order_id.state", string="Estado")

    sale_order_invoice_status = fields.Selection(related="sale_order_id.invoice_status", string="Estado Factura")