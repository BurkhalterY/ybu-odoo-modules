from odoo import api, fields, models


class ResParner(models.Model):
    _inherit = "res.partner"

    name_ids = fields.One2many("res.partner.name", "partner_id", string="Names")
    phone_ids = fields.One2many("res.partner.phone", "partner_id", string="Phones")
    email_ids = fields.One2many("res.partner.email", "partner_id", string="Emails")
    website_ids = fields.One2many(
        "res.partner.website", "partner_id", string="Websites"
    )

    phone = fields.Char(string="Phone", compute="_compute_phone", store=True)
    mobile = fields.Char(string="Mobile", compute="_compute_phone", store=True)
    email = fields.Char(string="Email", related="email_ids.name", store=True)
    website = fields.Char(related="website_ids.name", store=True)

    firstname = fields.Char("Firstname")
    lastname = fields.Char("Lastname")
    birthday = fields.Char("Birthday")
    gender = fields.Selection([("M", "Male"), ("F", "Female")], string="Gender")

    @api.depends("phone_ids")
    def _compute_phone(self):
        for partner in self:
            partner.phone = partner.phone_ids.filtered(
                lambda phone: "voice" in phone.type_ids.mapped("name")
            )[:1].name
            partner.mobile = partner.phone_ids.filtered(
                lambda phone: "cell" in phone.type_ids.mapped("name")
            )[:1].name

    def _mig_enhanced_fields(self):
        for model, ffields in (
            ("phone", ("phone", "mobile")),
            ("email", ("email",)),
            ("website", ("website",)),
        ):
            self.env[f"res.partner.{model}"].create(
                [
                    {
                        "partner_id": partner.id,
                        "name": getattr(partner, field),
                        **{"type": "cell" for _ in range(1) if field == "mobile"},
                    }
                    for field in ffields
                    for partner in self.with_context(active_test=False).search(
                        [(field, "!=", False)]
                    )
                ]
            )
