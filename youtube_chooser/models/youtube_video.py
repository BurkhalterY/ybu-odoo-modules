from odoo import fields, models


class YoutubeVideo(models.Model):
    _name = "youtube.video"
    _description = "YouTube Video"
    _order = "date desc"

    user_id = fields.Many2one("res.users", string="User")
    name = fields.Char("Title")
    url = fields.Char("URL")
    duration = fields.Float("Duration", help="Hours")
    channel = fields.Char("Channel")
    date = fields.Datetime("Release Date")

    playlist_id = fields.Many2one("youtube.playlist", string="Playlist")
    tag_ids = fields.Many2many("youtube.tag", string="Tags")
    viewed = fields.Boolean("Viewed")
