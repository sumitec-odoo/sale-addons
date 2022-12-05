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

    # Se utiliza en validacion de nivel
    # Algunos de los precios unitarios no coincide con la lista de precio
    # Porque se modificó o porque el presupuesto quedó desactualizado
    def correct_price(self):
        for order in self:
            incorrect_line = ""
            numero_linea = 0
            for line in order.order_line:
                numero_linea += 1
                correct_price = self.env['product.product'].browse(line.product_id.id).with_context(pricelist=order.pricelist_id.id).price
                if round(line.price_unit) != round(correct_price):
                    # TODO:
                    incorrect_line += str(numero_linea) + ", "

            if incorrect_line:
                notification_ids = []
                notification_ids.append((0,0,{
                    'res_partner_id': order.user_id.partner_id.id}))

                order.message_post(
                body="Líneas con precio incorrecto: {}".format(incorrect_line),
                message_type='notification',
                subtype_xmlid="mail.mt_comment",
                notification_ids=notification_ids)

                return False
            else:
                return True

    # lo uso en una validación de nivel de tipo Fórmula.
    # el código para controlar la fecha de vencimiento es: not rec.valid_quotation()
    def valid_quotation(self):
        for rec in self:
            delta = rec.validity_date - fields.Date.context_today(self)

            if delta.days >= 0:
                return True
            else:
                return False
