from odoo import api, fields, models


class ResParnerData(models.AbstractModel):
    _name = "res.partner.data"
    _description = "Partner Additional Data"
    _order = "sequence,name"

    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="cascade"
    )
    name = fields.Char("Value", required=True)
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

    type_ids = fields.Many2many("res.partner.phone.type")

    @api.onchange("name")
    def _onchange_phone_validation(self):
        if self.name:
            self.name = (
                self._phone_format(fname="name", force_format="INTERNATIONAL")
                or self.name
            )


class ResParnerPhoneType(models.Model):
    _name = "res.partner.phone.type"
    _description = "Phone Type"

    name = fields.Char("Technical Name", required=True)
    display_name = fields.Char("Name", required=True, translate=True)


class ResParnerEmail(models.Model):
    _name = "res.partner.email"
    _inherit = ["res.partner.data"]
    _description = "Partner Additional Email"


class ResParnerWebsite(models.Model):
    _name = "res.partner.website"
    _inherit = ["res.partner.data"]
    _description = "Partner Additional Website"
