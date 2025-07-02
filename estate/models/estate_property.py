from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties"

    name = fields.Char(
        string="Title",
        required=True,
    )

    description = fields.Text()

    postcode = fields.Char()

    date_availability = fields.Date(
        string="Available Date",
        copy=False,
        default=fields.Datetime.add(fields.Datetime.today(), months=+3)
    )

    expected_price = fields.Float(
        required=True
    )

    selling_price = fields.Float(
        readonly=True,
        copy=False
    )

    bedrooms = fields.Integer(
        default=2
    )

    living_erea = fields.Integer(
        string="Living Area (sqm)"
    )

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer(
        string="Garden Area (sqm)"
    )

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    state = fields.Selection(
        string="Status",
        selection=[
            ("new","New"),
            ("offer_received","Offer Received"),
            ("offer_accepted","Offer Accepted"),
            ("sold","Sold"),
            ("cancelled","Cancelled")
        ],
        required=True,
        default="new",
        copy=False
    )
    
    active = fields.Boolean(
        default=True
    )

    property_type_id = fields.Many2one(
        comodel_name="estate.property.type"
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesman",
        default= lambda self: self.env.user,
        copy=False
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer"
    )
