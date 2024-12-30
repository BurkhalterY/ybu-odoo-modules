from odoo import fields, models


class YoutubePlaylist(models.Model):
    _name = "youtube.playlist"
    _description = "YouTube PlayList/Channel"
    _order = "name"

    user_id = fields.Many2one("res.users", string="User")
    name = fields.Char("Name")
    url = fields.Char("URL")

    video_ids = fields.One2many("youtube.video", "playlist_id", string="Videos")
    tag_ids = fields.Many2many("youtube.tag", string="Tags")
