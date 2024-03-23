from uuid import uuid4

from odoo import api, fields, models

FUNC_TO_CALL = [
    (1, [1]),
    (7, [9]),
    (1, [i for i in range(3, 6)]),  # 6.1.  General Properties
    (2, [i for i in range(1, 8)]),  # 6.2.  Identification Properties
    (3, [i for i in range(1, 2)]),  # 6.3.  Delivery Addressing Properties
    (4, [i for i in range(1, 5)]),  # 6.4.  Communications Properties
    (5, [i for i in range(1, 3)]),  # 6.5.  Geographical Properties
    (6, [i for i in range(1, 3)]),  # 6.6.  Organizational Properties
    (7, [i for i in range(1, 9)]),  # 6.7.  Explanatory Properties
    (8, [i for i in range(1, 2)]),  # 6.8.  Security Properties
    (9, [i for i in range(1, 4)]),  # 6.9.  Calendar Properties
    (1, [2]),
]


class ResParner(models.Model):
    _inherit = "res.partner"

    uuid = fields.Char("UUID", index=True, required=True, readonly=True)
    vcard = fields.Text("vCard", compute="compute_vcard")

    _sql_constraints = [("uuid_uniq", "unique(uuid)", "An UUID is unique.")]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "uuid" not in vals_list:
                vals["uuid"] = uuid4()
        return super().create(vals_list)

    def compute_vcard(self):
        for partner in self:
            properties = []
            for i, jj in FUNC_TO_CALL:
                for j in jj:
                    properties += getattr(partner, f"_vcard_get_{6}_{i}_{j}")()

            vcard = ""
            for p in properties:
                params = "".join(
                    [f";{param[0]}={param[1]}" for param in p.get("parameters", [])]
                )
                vcard += f'{p["property"]}{params}:{p["value"]}\n'
            partner.vcard = vcard

    def _vcard_get_6_1_1(self):
        """BEGIN
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.1
        """
        self.ensure_one()
        return [{"property": "BEGIN", "value": "VCARD"}]

    def _vcard_get_6_1_2(self):
        """END
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.2
        """
        self.ensure_one()
        return [{"property": "END", "value": "VCARD"}]

    def _vcard_get_6_1_3(self):
        """SOURCE
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.3
        """
        self.ensure_one()
        if True:
            return []
        # TODO
        url = "https://directory.example.com/addressbooks/jdoe/Jean%20Dupont.vcf"
        return [{"property": "SOURCE", "value": url}]

    def _vcard_get_6_1_4(self):
        """KIND
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.4
        """
        self.ensure_one()
        return [
            {
                "property": "KIND",
                "value": "org" if self.is_company else "individual",
            }
        ]

    def _vcard_get_6_1_5(self):
        """XML
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.5
        """
        self.ensure_one()
        return []

    def _vcard_get_6_2_1(self):
        """FN
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.1
        """
        self.ensure_one()
        return [{"property": "FN", "value": self.name}]

    def _vcard_get_6_2_2(self):
        """N
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.2
        """
        self.ensure_one()
        family_names = (self.lastname or "").replace(" ", ",")
        given_names = (self.firstname or "").split(" ", 1)[0]
        additional_names = ",".join((self.firstname or "").split(" ")[1:])
        honorific_prefixes = self.title.shortcut or ""
        honorific_suffixes = ""
        return [
            {
                "property": "N",
                "value": ";".join(
                    [
                        family_names,
                        given_names,
                        additional_names,
                        honorific_prefixes,
                        honorific_suffixes,
                    ]
                ),
            }
        ]

    def _vcard_get_6_2_3(self):
        """NICKNAME
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.3
        """
        self.ensure_one()
        if True:
            return []
        # TODO
        return [
            {
                "property": "NICKNAME",
                "value": ",".join(self.aka_ids.mapped("name")),
            }
        ]

    def _vcard_get_6_2_4(self):
        """PHOTO
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.4
        """
        self.ensure_one()
        if True:
            return []
        # TODO base url + uuid
        return [
            {
                "property": "PHOTO",
                "value": ("https://www.example.com/pub/photos/jqpublic.gif"),
            }
        ]

    def _vcard_get_6_2_5(self):
        """BDAY
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.5
        """
        self.ensure_one()
        properties = []
        if False:
            properties.append(
                {
                    "property": "BDAY",
                    "value": "date-and-or-time",  # TODO
                }
            )
        return properties

    def _vcard_get_6_2_6(self):
        """ANNIVERSARY
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.6
        """
        self.ensure_one()
        return []

    def _vcard_get_6_2_7(self):
        """GENDER
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.7
        """
        self.ensure_one()
        if not self.env["ir.module.module"].search_count(
            [("name", "=", "partner_contact_gender"), ("state", "=", "installed")],
            limit=1,
        ):
            # Skip if Contact gender (OCA) is not installed
            return []
        gender = (
            "N"
            if self.is_company
            else {
                "male": "M",
                "female": "F",
                "other": "O",
            }.get(self.gender, "U")
        )
        return [{"property": "GENDER", "value": gender}]

    def _vcard_get_6_3_1(self):
        """ADR
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.3.1
        """
        self.ensure_one()
        properties = []
        if self.street or self.city or self.state_id or self.zip or self.country_id:
            properties.append(
                {
                    "property": "ADR",
                    "value": ";".join(
                        [
                            "",
                            "",
                            self.street,
                            self.city,
                            self.state_id.name or "",
                            self.zip,
                            self.country_id.name or "",
                        ]
                    ),
                }
            )
        return properties

    def _vcard_get_6_4_1(self):
        """TEL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1
        """
        self.ensure_one()
        properties = []
        if self.phone:
            properties.append(
                {
                    "property": "TEL",
                    "parameters": {("VALUE", "uri"), ("TYPE", "voice"), ("PREF", "1")},
                    "value": f"tel:{self.phone}",
                }
            )
        if self.mobile:
            properties.append(
                {
                    "property": "TEL",
                    "parameters": {("VALUE", "uri"), ("TYPE", "cell")},
                    "value": f"tel:{self.mobile}",
                }
            )
        return properties

    def _vcard_get_6_4_2(self):
        """EMAIL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2
        """
        self.ensure_one()
        properties = []
        if self.email:
            properties.append(
                {
                    "property": "EMAIL",
                    "parameters": {("PREF", "1")},
                    "value": self.email,
                }
            )
        return properties

    def _vcard_get_6_4_3(self):
        """IMPP
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.3
        """
        self.ensure_one()
        return []

    def _vcard_get_6_4_4(self):
        """LANG
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.4
        """
        self.ensure_one()
        if not self.lang:
            return []
        return [{"property": "LANG", "value": self.lang[:2]}]

    def _vcard_get_6_5_1(self):
        """TZ
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.5.1
        """
        self.ensure_one()
        return []

    def _vcard_get_6_5_2(self):
        """GEO
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.5.2
        """
        self.ensure_one()
        if not (self.partner_latitude or self.partner_longitude):
            # Null Island would be a false positive, but ¯\_(ツ)_/¯
            return []
        geo = f"geo:{self.partner_latitude},{self.partner_longitude}"
        return [{"property": "GEO", "value": geo}]

    def _vcard_get_6_6_1(self):
        """TITLE
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.1
        """
        self.ensure_one()
        if not self.function:
            return []
        return [{"property": "TITLE", "value": self.function}]

    def _vcard_get_6_6_2(self):
        """ROLE
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.2
        """
        self.ensure_one()
        return []

    def _vcard_get_6_6_3(self):
        """LOGO
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.3
        """
        self.ensure_one()
        if True:
            return []
        # TODO base url + uuid (parent_id)
        return [
            {
                "property": "LOGO",
                "value": "https://www.example.com/pub/photos/jqpublic.gif",
            }
        ]

    def _vcard_get_6_6_4(self):
        """ORG
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.4
        """
        self.ensure_one()
        if not self.company_name:
            return []
        return [{"property": "ORG", "value": self.company_name}]

    def _vcard_get_6_6_5(self):
        """MEMBER
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.5
        """
        self.ensure_one()
        return []

    def _vcard_get_6_6_6(self):
        """RELATED
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.6
        """
        self.ensure_one()
        return []

    def _vcard_get_6_7_1(self):
        """CATEGORIES
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.1
        """
        self.ensure_one()
        if not self.category_id:
            return []
        categories = ",".join(self.category_id.mapped("name"))
        return [{"property": "CATEGORIES", "value": categories}]

    def _vcard_get_6_7_2(self):
        """NOTE
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.2
        """
        self.ensure_one()
        if not self.comment:
            return []
        return [{"property": "NOTE", "value": self.comment}]

    def _vcard_get_6_7_3(self):
        """PRODID
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.3
        """
        self.ensure_one()
        return []

    def _vcard_get_6_7_4(self):
        """REV
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.4
        """
        self.ensure_one()
        ts = self.write_date.strftime("%Y%m%dT%H%M%SZ")
        return [{"property": "REV", "value": ts}]

    def _vcard_get_6_7_5(self):
        """SOUND
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.5
        """
        self.ensure_one()
        return []

    def _vcard_get_6_7_6(self):
        """UID
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.6
        """
        self.ensure_one()
        return [{"property": "UID", "value": f"urn:uuid:{self.uuid}"}]

    def _vcard_get_6_7_7(self):
        """CLIENTPIDMAP
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.7
        """
        self.ensure_one()
        return []

    def _vcard_get_6_7_8(self):
        """URL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.8
        """
        self.ensure_one()
        properties = []
        if self.website:
            properties.append(
                {
                    "property": "URL",
                    "parameters": {("PREF", "1")},
                    "value": self.website,
                }
            )
        return properties

    def _vcard_get_6_7_9(self):
        """VERSION
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.9
        """
        self.ensure_one()
        return [{"property": "VERSION", "value": "4.0"}]

    def _vcard_get_6_8_1(self):
        """KEY
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.8.1
        """
        self.ensure_one()
        return []

    def _vcard_get_6_9_1(self):
        """FBURL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.1
        """
        self.ensure_one()
        return []

    def _vcard_get_6_9_2(self):
        """CALADRURI
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.2
        """
        self.ensure_one()
        return []

    def _vcard_get_6_9_3(self):
        """CALURI
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.3
        """
        self.ensure_one()
        return []
