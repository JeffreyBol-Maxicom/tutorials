from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils, float_utils


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _order = "price desc"

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

    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "An offer price must be strictly positive")
    ]

    @api.model_create_multi
    def create(self, vals):
        for offer in vals:
            prop = self.env['estate.property'].browse(offer['property_id'])
            # ensure new offer is higher then existing offers
            if float_utils.float_compare(offer['price'], prop.best_offer, precision_digits=2) <= 0:
                raise UserError(f"Price has to be higher then the current best offer: {float_utils.float_repr(prop.best_offer, precision_digits=2)}")
            prop.state = 'offer_received'
        return super().create(vals)

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
            # get all offers for property
            property_offers = self.env['estate.property.offer'].search([("property_id", "=", record.property_id.id)])
            # only one accepted offer allowed
            if property_offers.filtered(lambda offer: offer.status == "accepted" and offer.id != record.id):
                raise UserError('Another offer already accepted')
            # Accept selected offer
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = "offer_accepted"
            # Refuse all other offers
            property_offers.filtered(lambda offer: offer.status != "accepted").action_refuse()
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
