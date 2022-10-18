from odoo import api, fields, models
from odoo.tools.translate import html_translate

# src/addons/sale_quotation_builder/models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    website_description_2 = fields.Html('Website Description 2', sanitize_attributes=False, translate=html_translate)

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        ret = super(SaleOrder, self).onchange_sale_order_template_id()
        if self.sale_order_template_id:
            template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
            # import pdb; pdb.set_trace()
            self.website_description_2 = template.website_description_2
        return ret