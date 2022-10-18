from odoo import api, fields, models
from odoo.tools.translate import html_translate

# src/addons/sale_quotation_builder/models/sale_order_template.py:8
class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    website_description_2 = fields.Html('Website Description 2', translate=html_translate, sanitize_attributes=False)

