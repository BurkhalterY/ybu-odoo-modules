from odoo import fields, models


class YoutubeTag(models.Model):
    _name = "youtube.tag"
    _description = "YouTube Tag"
    _order = "name"

    user_id = fields.Many2one("res.users", string="User")
    name = fields.Char("Tag")
    active = fields.Boolean(default=True)
