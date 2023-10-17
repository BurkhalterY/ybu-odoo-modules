from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    link_ids = fields.One2many("link.link", "res_id", string="Links")
