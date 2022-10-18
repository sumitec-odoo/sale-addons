# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ['sale.order', 'tier.validation']

    user_requesting_review = fields.Many2one('res.users',string="Usuario que solicita la revisión")

    def _notify_accepted_reviews(self):
        super(SaleOrder,self)._notify_accepted_reviews()
        notification_ids = []
        notification_ids.append((0,0,{
                'res_partner_id':self.user_requesting_review.partner_id.id}))        
        self.message_post(
            body='Se aprobo su pedido de revisión!', 
            message_type='notification', 
            subtype='mail.mt_comment',
            notification_ids=notification_ids)

    @api.multi
    def request_validation(self):
        self.user_requesting_review = self.env.user
        super(SaleOrder,self).request_validation()