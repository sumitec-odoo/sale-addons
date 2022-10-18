from odoo import SUPERUSER_ID, fields, api

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    sale_order_ids = env['sale.order'].search([]).filtered(lambda x: x.review_ids)

    for so in sale_order_ids:
        if not so.review_done_by_users:            
            cr.execute('UPDATE sale_order SET review_done_by_users=%s WHERE id=%s',(', '.join(so.review_ids.mapped("done_by.name")),so.id,))

        if not so.definicion_nivel:
            cr.execute('UPDATE sale_order SET definicion_nivel=%s WHERE id=%s',(', '.join(so.review_ids.mapped("definition_id.name")),so.id,))

# Cuidado con el módulo sale_order_quote
# con el migrate se dispara el write de ese módulo en cada uno de los so modificados
# y borra las lineas del log. pero no debería pasar si el estado es bloqueado (done)??
# por eso lo hago directo por SQL y así evito ese problema (y se hace mucho más rápido)
