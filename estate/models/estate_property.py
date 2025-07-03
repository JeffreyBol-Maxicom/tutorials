from odoo import api, fields, models


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

    living_area = fields.Integer(
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

    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
    )

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers"
    )

    total_area = fields.Integer(
        compute="_compute_total_area",
        string="Total Area (sqm)"
    )

    best_offer = fields.Float(
        compute="_compute_best_offer"
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            prices = self.offer_ids.mapped('price')
            record.best_offer = max(prices)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else None
