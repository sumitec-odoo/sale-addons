# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderMpeProductSrc(models.Model):
    _name = 'sale.order.mpe.product.src'
    # _order = 'id desc'
    _description = 'Productos Intercambiables - Origen'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "src_product_id"

    src_product_id = fields.Many2one('product.product', string='Producto Origen')

    dest_product_ids = fields.One2many('sale.order.mpe.product.dest', 'mpe_product_src_id', string='Destino')