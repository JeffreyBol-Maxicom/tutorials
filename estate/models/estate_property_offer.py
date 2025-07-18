from odoo import api, fields, models
from odoo.exceptions import UserError
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

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "An offer price must be strictly positive")
    ]

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

    def action_accept(self):
        for record in self:
            # nothing to do if current record already accepted
            if record.status == "accepted":
                return True
            # get all offers for property
            property_offers = self.env['estate.property.offer'].search([("property_id", "=", record.property_id.id)])
            # only one accepted offer allowed
            if property_offers.filtered(lambda offer: offer.status == "accepted"):
                raise UserError('Another offer already accepted')
            # Accept selected offer
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            # Refuse all other offers
            property_offers.filtered(lambda offer: offer.status != "accepted").action_refuse()
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.partner_id = None
            record.status = "refused"
        return True
