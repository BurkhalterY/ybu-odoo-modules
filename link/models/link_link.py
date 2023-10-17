import logging

import requests
from lxml.html import document_fromstring
from odoo import api, fields, models

logger = logging.getLogger(__name__)


class LinkLink(models.Model):
    _name = "link.link"
    _description = "Link"
    _order = "sequence"

    res_model = fields.Char("Related Model", required=True, index=True)
    res_id = fields.Many2oneReference(
        "Related Document ID", model_field="res_model", index=True
    )
    name = fields.Char("URL", required=True)
    description = fields.Char(
        "Description", compute="_compute_description", store=True, readonly=False
    )
    sequence = fields.Integer("Sequence", default=10)
    favorite = fields.Selection(
        [("0", "No"), ("1", "Yes")], string="Favorite", required=True, default="0"
    )

    @api.depends("name")
    def _compute_description(self):
        for link in self.filtered("name"):
            if "://" not in link.name:
                link.name = "https://" + link.name
            try:
                r = requests.get(link.name)
                link.description = document_fromstring(r.text).find(".//title").text
            except Exception as err:
                logger.error(err)

    def open_url(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": self.name,
            "target": "new",
        }
