from odoo import models, fields, api


class SaleAgentWizard(models.TransientModel):
    _name = "sale.order.agent.wizard"
    _description = "Sale order Agent Wizard"

    agent = fields.Many2one(string="Agente",comodel_name="res.partner",domain=[('agent', '=', True)])

    def confirm(self):
        self.ensure_one()
        order = self.env['sale.order'].browse(
            self._context.get('active_id', False))

        for line in order.order_line:
            if self.agent:
                vals = {
                    'agent_id': self.agent.id,
                    'commission_id': self.agent.commission_id.id,
                    'object_id': line.id
                }
                line.agent_ids.create(vals)
            else:
                line.agent_ids.unlink()
        
        return True