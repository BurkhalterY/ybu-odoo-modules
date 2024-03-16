from odoo import api, fields, models


class ResParnerData(models.AbstractModel):
    _name = "res.partner.data"
    _description = "Partner Additional Data"
    _order = "sequence,name"

    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="cascade"
    )
    name = fields.Char("Value", required=True)
    type = fields.Selection(
        [("work", "Work"), ("home", "Home")],
        string="Type",
        help="Let empty for both",
    )
    note = fields.Text("Note")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)


class ResParnerName(models.Model):
    _name = "res.partner.name"
    _inherit = ["res.partner.data"]
    _description = "Partner Additional Name"


class ResParnerPhone(models.Model):
    _name = "res.partner.phone"
    _inherit = ["res.partner.data"]
    _description = "Partner Additional Phone"

    type2 = fields.Selection(
        [
            ("text", "Text"),
            ("voice", "Voice"),
            ("fax", "Fax"),
            ("cell", "Cell"),
            ("video", "Video"),
            ("pager", "Pager"),
            ("textphone", "Textphone"),
        ],
        string="Phone Type",
        default="voice",
        required=True,
    )

    @api.onchange("name", "partner_id.country_id", "partner_id.company_id")
    def _onchange_phone_validation(self):
        if self.name:
            self.name = (
                self._phone_format(fname="name", force_format="INTERNATIONAL")
                or self.name
            )


class ResParnerEmail(models.Model):
    _name = "res.partner.email"
    _inherit = ["res.partner.data"]
    _description = "Partner Additional Email"


class ResParnerWebsite(models.Model):
    _name = "res.partner.website"
    _inherit = ["res.partner.data"]
    _description = "Partner Additional Website"
