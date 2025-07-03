from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


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
        required=True,
        ondelete="cascade"
    )

    validity = fields.Integer(
        default=7
    )

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = date_utils.add(create_date, days=+record.validity)        

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(
                record.create_date if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - create_date).days
