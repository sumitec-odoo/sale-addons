# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_image = fields.Boolean(
        "Imprimir imagen",
        default=True,
        help="Si está tildado, se muestran las imagenes de los productos en el presupuesto Web",
    )
