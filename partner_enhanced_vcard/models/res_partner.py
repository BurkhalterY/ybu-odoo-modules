from odoo import api, fields, models


class ResParner(models.Model):
    _inherit = "res.partner"

    def _vcard_get_6_4_1(self):
        """TEL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1
        """
        self.ensure_one()
        properties = []
        for phone in self.phone_ids:
            properties.append(
                {
                    "property": "TEL",
                    "parameters": {("VALUE", "uri"), ("TYPE", phone.type)},
                    "value": f"tel:{phone.name}",
                }
            )
        if properties:
            properties[0]["parameters"].add(("PREF", "1"))
        return properties

    def _vcard_get_6_4_2(self):
        """EMAIL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2
        """
        self.ensure_one()
        properties = []
        for email in self.email_ids:
            properties.append(
                {
                    "property": "EMAIL",
                    "value": email.name,
                }
            )
        if properties:
            properties[0]["parameters"] = {("PREF", "1")}
        return properties

    # def _vcard_get_6_4_3(self):
    #     """IMPP
    #     https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.3
    #     """
    #     self.ensure_one()
    #     return []

    def _vcard_get_6_7_8(self):
        """URL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.8
        """
        self.ensure_one()
        properties = []
        for website in self.website_ids:
            properties.append(
                {
                    "property": "URL",
                    "value": website.name,
                }
            )
        return properties
