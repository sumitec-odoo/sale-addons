# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ['sale.order', 'tier.validation']

    review_done_by_users = fields.Char(string='Aprobado Por')
    definicion_nivel = fields.Char(string='Definición de nivel')

    def _validate_tier(self, tiers=False):
        super(SaleOrder,self)._validate_tier()
        self.review_done_by_users = ', '.join(self.review_ids.mapped("done_by.name"))
        self.definicion_nivel = ', '.join(self.review_ids.mapped("definition_id.name"))
        # import pdb; pdb.set_trace()        

    @api.model
    def _get_under_validation_exceptions(self):
        res = super(SaleOrder,self)._get_under_validation_exceptions()
        # estos campos no los va a tener en cuenta para la validación
        res.append('review_done_by_users')
        res.append('definicion_nivel')
        return res

    def restart_validation(self):
        super(SaleOrder,self).restart_validation()
        for rec in self:
            rec.review_done_by_users = False
            rec.definicion_nivel = False
