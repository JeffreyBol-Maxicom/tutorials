from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"

    price = fields.Float()

    status = fields.Selection(
        selection=[
            ("accepted","Accepted"),
            ("refused","Refused")
        ],
        copy=False
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        required=True
    )

    property_id = fields.Many2one(
        comodel_name="estate.property",
        required=True
    )
