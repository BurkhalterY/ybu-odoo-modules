from uuid import uuid4

from odoo import api, fields, models

FUNC_TO_CALL = (
    "_get_vcard_begin",
    "_get_vcard_version",
    "_get_vcard_source",
    "_get_vcard_kind",
    "_get_vcard_xml",
    "_get_vcard_fn",
    "_get_vcard_n",
    "_get_vcard_nickname",
    "_get_vcard_photo",
    "_get_vcard_bday",
    "_get_vcard_anniversary",
    "_get_vcard_gender",
    "_get_vcard_adr",
    "_get_vcard_tel",
    "_get_vcard_email",
    "_get_vcard_mailer",
    "_get_vcard_impp",
    "_get_vcard_lang",
    "_get_vcard_tz",
    "_get_vcard_geo",
    "_get_vcard_title",
    "_get_vcard_role",
    "_get_vcard_logo",
    "_get_vcard_agent",
    "_get_vcard_org",
    "_get_vcard_member",
    "_get_vcard_related",
    "_get_vcard_categories",
    "_get_vcard_note",
    "_get_vcard_prodid",
    "_get_vcard_rev",
    "_get_vcard_sort_string",
    "_get_vcard_sound",
    "_get_vcard_uid",
    "_get_vcard_clientpidmap",
    "_get_vcard_url",
    "_get_vcard_class",
    "_get_vcard_key",
    "_get_vcard_fburl",
    "_get_vcard_caladruri",
    "_get_vcard_caluri",
    "_get_vcard_end",
)

DEFAULT_VCARD_VERSION = 3


class ResParner(models.Model):
    _inherit = "res.partner"

    uuid = fields.Char("UUID", index=True, required=True, readonly=True)
    vcard = fields.Text("vCard", compute="compute_vcard")

    _sql_constraints = [("uuid_uniq", "unique(uuid)", "An UUID is unique.")]

    @api.model
    def vcard_version(self):
        return self.env.context.get("vcard_version", DEFAULT_VCARD_VERSION)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "uuid" not in vals_list:
                vals["uuid"] = uuid4()
        return super().create(vals_list)

    def compute_vcard(self):
        for partner in self:
            properties = []
            for f in FUNC_TO_CALL:
                properties += getattr(partner, f)()

            vcard = ""
            for p in properties:
                params = "".join(
                    [f";{param[0]}={param[1]}" for param in p.get("parameters", [])]
                )
                vcard += f'{p["property"]}{params}:{p["value"]}\n'
            partner.vcard = vcard

    def _get_vcard_begin(self):
        """BEGIN
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.1
        """
        self.ensure_one()
        return [{"property": "BEGIN", "value": "VCARD"}]

    def _get_vcard_end(self):
        """END
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.2
        """
        self.ensure_one()
        return [{"property": "END", "value": "VCARD"}]

    def _get_vcard_source(self):
        """SOURCE
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.3
        """
        self.ensure_one()
        if True:
            return []
        # TODO
        url = "https://directory.example.com/addressbooks/jdoe/Jean%20Dupont.vcf"
        return [{"property": "SOURCE", "value": url}]

    def _get_vcard_kind(self):
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

    def _get_vcard_xml(self):
        """XML
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.1.5
        """
        self.ensure_one()
        return []

    def _get_vcard_fn(self):
        """FN
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.1.1
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.1
        """
        self.ensure_one()
        return [{"property": "FN", "value": self.name}]

    def _get_vcard_n(self):
        """N
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.1.2
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

    def _get_vcard_nickname(self):
        """NICKNAME
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.1.3
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.3
        """
        self.ensure_one()
        return []

    def _get_vcard_photo(self):
        """PHOTO
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.1.4
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.4
        """
        self.ensure_one()
        if True:
            return []
        # TODO base url + uuid
        p = {
            "property": "PHOTO",
            "value": ("https://www.example.com/pub/photos/jqpublic.gif"),
        }
        if self.vcard_version() == 3:
            p["parameters"] = {("VALUE", "uri")}
        return [p]

    def _get_vcard_bday(self):
        """BDAY
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.1.5
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

    def _get_vcard_anniversary(self):
        """ANNIVERSARY
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.6
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []  # Exists only in vCard 4
        return []

    def _get_vcard_gender(self):
        """GENDER
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.2.7
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []  # Exists only in vCard 4

        if not self.env["ir.module.module"].search_count(
            [("name", "=", "partner_contact_gender"), ("state", "=", "installed")],
            limit=1,
        ):
            return []  # Skip if Contact gender (OCA) is not installed

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

    def _get_vcard_adr(self):
        """ADR
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.2.1
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.2.2
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.3.1
        """
        self.ensure_one()
        properties = []
        if self.street or self.city or self.state_id or self.zip or self.country_id:
            p = {
                "property": "ADR",
                "value": ";".join(
                    [
                        "",  # post office box
                        "",  # extended address
                        self.street,  # street address
                        self.city,  # locality
                        self.state_id.name or "",  # region
                        self.zip,  # postal code
                        self.country_id.name or "",  # country name
                    ]
                ),
            }
            properties.append(p)

            label = (
                self.name
                + "\\n"
                + self._display_address(without_company=True).replace("\n", "\\n")
            )
            if self.vcard_version() == 3:
                properties.append({"property": "LABEL", "value": label})
            elif self.vcard_version() == 4:
                p["parameters"] = {("LABEL", label)}
        return properties

    def _get_vcard_tels(self):
        return [
            {"name": self.phone, "types": ["voice"]},
            {"name": self.mobile, "types": ["cell"]},
        ]

    def _get_vcard_tel(self):
        """TEL
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.3.1
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.1
        """
        self.ensure_one()
        properties = []
        pref = True
        for number in self._get_vcard_tels():
            if not number["name"]:
                continue
            if self.vcard_version() == 3:
                number["types"] = ["msg" if t == "text" else t for t in number["types"]]
                if pref:
                    number["types"].append("pref")
                    pref = False
                p = {
                    "property": "TEL",
                    "parameters": {("TYPE", ",".join(number["types"]))},
                    "value": number["name"],
                }
            elif self.vcard_version() == 4:
                number["types"] = [
                    "text" if t == "msg" else t for t in number["types"]
                ]  # Should not be triggered with default data
                p = {
                    "property": "TEL",
                    "parameters": {
                        ("VALUE", "uri"),
                        ("TYPE", ",".join(number["types"])),
                    },
                    "value": f'tel:{number["name"]}',
                }
                if pref:
                    p["parameters"].add(("PREF", "1"))
                    pref = False
            properties.append(p)
        return properties

    def _get_vcard_emails(self):
        return [self.email]

    def _get_vcard_email(self):
        """EMAIL
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.3.2
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.2
        """
        self.ensure_one()
        properties = []
        pref = True
        for email in self._get_vcard_emails():
            if not email:
                continue
            if self.vcard_version() == 3:
                types = ["internet"]
                if pref:
                    types.append("pref")
                    pref = False
                p = {
                    "property": "EMAIL",
                    "parameters": {("TYPE", ",".join(types))},
                    "value": email,
                }
            elif self.vcard_version() == 4:
                p = {
                    "property": "EMAIL",
                    "value": email.name,
                }
                if pref:
                    p["parameters"] = {("PREF", "1")}
                    pref = False
            properties.append(p)
        return properties

    def _get_vcard_mailer(self):
        """MAILER
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.3.3
        """
        self.ensure_one()
        if self.vcard_version() != 3:
            return []
        return []

    def _get_vcard_impp(self):
        """IMPP
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.3
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        return []

    def _get_vcard_lang(self):
        """LANG
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.4.4
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        if not self.lang:
            return []
        return [{"property": "LANG", "value": self.lang[:2]}]

    def _get_vcard_tz(self):
        """TZ
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.4.1
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.5.1
        """
        self.ensure_one()
        return []

    def _get_vcard_geo(self):
        """GEO
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.4.2
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.5.2
        """
        self.ensure_one()
        if not (self.partner_latitude or self.partner_longitude):
            # Null Island would be a false positive, but ¯\_(ツ)_/¯
            return []

        if self.vcard_version() == 3:
            geo = f"{self.partner_latitude};{self.partner_longitude}"
        elif self.vcard_version() == 4:
            geo = f"geo:{self.partner_latitude},{self.partner_longitude}"
        return [{"property": "GEO", "value": geo}]

    def _get_vcard_title(self):
        """TITLE
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.5.1
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.1
        """
        self.ensure_one()
        if not self.function:
            return []
        return [{"property": "TITLE", "value": self.function}]

    def _get_vcard_role(self):
        """ROLE
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.5.2
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.2
        """
        self.ensure_one()
        return []

    def _get_vcard_logo(self):
        """LOGO
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.5.3
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.3
        """
        self.ensure_one()
        if True:
            return []
        # TODO base url + uuid (parent_id)
        p = {
            "property": "LOGO",
            "value": ("https://www.example.com/pub/photos/jqpublic.gif"),
        }
        if self.vcard_version() == 3:
            p["parameters"] = {("VALUE", "uri")}
        return [p]

    def _get_vcard_agent(self):
        """AGENT
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.5.4
        """
        self.ensure_one()
        if self.vcard_version() == 4:
            return []
        return []

    def _get_vcard_org(self):
        """ORG
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.5.5
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.4
        """
        self.ensure_one()
        if not self.company_name:
            return []
        return [{"property": "ORG", "value": self.company_name}]

    def _get_vcard_member(self):
        """MEMBER
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.5
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        return []

    def _get_vcard_related(self):
        """RELATED
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.6.6
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        return []

    def _get_vcard_categories(self):
        """CATEGORIES
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.1
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.1
        """
        self.ensure_one()
        if not self.category_id:
            return []
        categories = ",".join(self.category_id.mapped("name"))
        return [{"property": "CATEGORIES", "value": categories}]

    def _get_vcard_note(self):
        """NOTE
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.2
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.2
        """
        self.ensure_one()
        if not self.comment:
            return []
        return [{"property": "NOTE", "value": self.comment}]

    def _get_vcard_prodid(self):
        """PRODID
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.3
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.3
        """
        self.ensure_one()
        return []

    def _get_vcard_rev(self):
        """REV
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.4
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.4
        """
        self.ensure_one()
        if self.vcard_version() == 3:
            ts = self.write_date.isoformat()[:19] + "Z"
        elif self.vcard_version() == 4:
            ts = self.write_date.strftime("%Y%m%dT%H%M%SZ")
        return [{"property": "REV", "value": ts}]

    def _get_vcard_sort_string(self):
        """SORT-STRING
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.5.4
        """
        self.ensure_one()
        if self.vcard_version() == 4:
            return []
        return []

    def _get_vcard_sound(self):
        """SOUND
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.6
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.5
        """
        self.ensure_one()
        return []

    def _get_vcard_uid(self):
        """UID
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.7
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.6
        """
        self.ensure_one()
        return [{"property": "UID", "value": f"urn:uuid:{self.uuid}"}]

    def _get_vcard_clientpidmap(self):
        """CLIENTPIDMAP
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.7
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        return []

    def _get_vcard_urls(self):
        return [self.website]

    def _get_vcard_url(self):
        """URL
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.8
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.8
        """
        self.ensure_one()
        properties = []
        pref = self.vcard_version() == 4
        for website in self._get_vcard_urls():
            if not website:
                continue
            p = {
                "property": "URL",
                "value": website,
            }
            if pref and self.vcard_version() == 4:
                p["parameters"] = {("PREF", "1")}
                pref = False
            properties.append(p)
        return properties

    def _get_vcard_version(self):
        """VERSION
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.6.9
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.7.9
        """
        self.ensure_one()
        if self.vcard_version() == 3:
            v = "3.0"
        elif self.vcard_version() == 4:
            v = "4.0"
        return [{"property": "VERSION", "value": v}]

    def _get_vcard_class(self):
        """CLASS
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.7.1
        """
        self.ensure_one()
        if self.vcard_version() == 4:
            return []
        values = ("PUBLIC", "PRIVATE", "CONFIDENTIAL")
        return [{"property": "CLASS", "value": values[0]}]

    def _get_vcard_key(self):
        """KEY
        https://datatracker.ietf.org/doc/html/rfc2426#section-3.7.2
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.8.1
        """
        self.ensure_one()
        return []

    def _get_vcard_fburl(self):
        """FBURL
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.1
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        return []

    def _get_vcard_caladruri(self):
        """CALADRURI
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.2
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        return []

    def _get_vcard_caluri(self):
        """CALURI
        https://datatracker.ietf.org/doc/html/rfc6350#section-6.9.3
        """
        self.ensure_one()
        if self.vcard_version() != 4:
            return []
        return []
