from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    youtube_api_key = fields.Char("YouTube API Key")
