from odoo import Command, fields, models

class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            self.env['account.move'].sudo().create({
                "partner_id": record.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": (record.selling_price * 0.06)
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": float(100)
                    })
                ]
            })
        return super().action_sold()

