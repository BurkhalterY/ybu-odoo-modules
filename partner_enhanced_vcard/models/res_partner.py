from odoo import models


class ResParner(models.Model):
    _inherit = "res.partner"

    def _get_vcard_tels(self):
        return [
            {
                "name": phone.name,
                "types": phone.type_ids.mapped("name"),
            }
            for phone in self.phone_ids
        ]

    def _get_vcard_emails(self):
        return self.email_ids.mapped("name")

    def _get_vcard_urls(self):
        return self.website_ids.mapped("name")

    def _get_vcard_nickname(self):
        return [
            {
                "property": "NICKNAME",
                "value": ",".join(self.name_ids.mapped("name")),
            }
        ]
