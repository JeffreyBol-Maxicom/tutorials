from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"

    name = fields.Char(
        required=True
    )
