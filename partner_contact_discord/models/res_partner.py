import logging

import requests
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    discord_uid = fields.Char(string="Discord ID")
    discord_tag = fields.Char(
        string="Discord", compute="compute_discord_tag", store=True
    )

    @api.depends("discord_uid")
    def compute_discord_tag(self):
        for partner in self.filtered("discord_uid"):
            try:
                r = requests.get(
                    f"https://discordlookup.mesavirep.xyz/v1/user/{partner.discord_uid}"
                )
                partner.discord_tag = r.json().get("tag")
            except Exception as err:
                logger.error(err)

    def contact_via_discord(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": f"https://discordapp.com/users/{self.discord_uid}",
            "target": "new",
        }
