from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    youtube_api_key = fields.Char(related="company_id.youtube_api_key", readonly=False)
