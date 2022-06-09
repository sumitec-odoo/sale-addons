# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderMpeProductDest(models.Model):
    _name = 'sale.order.mpe.product.dest'
    _order = 'id desc'
    # _description = 'Cambio masivo de producto'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "dest_product_id"

    mpe_product_src_id = fields.Many2one("sale.order.mpe.product.src", string="Origen")
    
    dest_product_id = fields.Many2one('product.product', string='Producto Destino')