from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _order ="sequence, name, id"

    name = fields.Char(
        required=True
    )

    property_id = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id"
    )

    sequence = fields.Integer(
        default=1,
        help="Used to order the property types, lower is better."
    )

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id"
    )

    offer_count = fields.Integer(
        compute="_compute_offer_count"
    )

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "A property type name must be unique")
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
