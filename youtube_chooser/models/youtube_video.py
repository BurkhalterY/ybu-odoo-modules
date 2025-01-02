import base64
from datetime import datetime

import requests
from odoo import api, fields, models
from odoo.addons.youtube_chooser.utils.utils import iso8601_to_minutes


class YoutubeVideo(models.Model):
    _name = "youtube.video"
    _description = "YouTube Video"
    _order = "date desc"

    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.uid
    )
    name = fields.Char("Title")
    url = fields.Char("URL", required=True)
    youtubeid = fields.Char("YouTube ID", compute="_compute_youtubeid", store=True)
    duration = fields.Float("Duration", help="Hours")
    channel = fields.Char("Channel")
    date = fields.Datetime("Release Date")
    lang_id = fields.Many2one("res.lang", string="Language")
    thumbnail = fields.Binary("Thumbnail")

    playlist_id = fields.Many2one("youtube.playlist", string="Playlist")
    tag_ids = fields.Many2many("youtube.tag", string="Tags")
    viewed = fields.Boolean("Viewed")

    _sql_constraints = [
        (
            "uniq_youtubeid",
            "UNIQUE(user_id, youtubeid)",
            "Playlist YouTube ID must be unique.",
        ),
    ]

    @api.depends("url")
    def _compute_youtubeid(self):
        for video in self:
            if "watch" in video.url and "v=" in video.url:
                video.youtubeid = video.url.split("v=")[1].split("&")[0]
            elif video.url.startswith("https://youtu.be/"):
                video.youtubeid = video.url.split(".be/")[1].split("?")[0]

    def sync(self):
        api_url = "https://www.googleapis.com/youtube/v3/videos"
        for video in self.filtered("youtubeid"):
            params = {
                "part": "snippet,contentDetails",
                "id": video.youtubeid,
                "key": self.env.company.youtube_api_key,
            }
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue
            data = response.json()
            if "items" not in data:
                continue
            for item in data["items"]:
                lang_code = item["snippet"]["defaultAudioLanguage"][:2]
                print(lang_code)
                lang = (
                    self.env["res.lang"]
                    .with_context(active_test=False)
                    .search([("iso_code", "=", lang_code)])
                )
                print(lang)
                thumbnails = item["snippet"]["thumbnails"]
                thumbnail_url = (
                    thumbnails["high"]["url"]
                    if "high" in thumbnails
                    else thumbnails["default"]["url"]
                )
                thumbnail_response = requests.get(thumbnail_url, stream=True)
                thumbnail_content = (
                    base64.b64encode(thumbnail_response.content)
                    if thumbnail_response.status_code == 200
                    else False
                )
                video.write(
                    {
                        "name": item["snippet"]["title"],
                        "duration": iso8601_to_minutes(
                            item.get("contentDetails", {}).get("duration")
                        ),
                        "channel": item["snippet"]["channelTitle"],
                        "date": datetime.fromisoformat(
                            item["snippet"]["publishedAt"].replace("Z", "")
                        ),
                        "lang_id": lang.id if lang else False,
                        "thumbnail": thumbnail_content,
                    }
                )

    def watch(self):
        self.ensure_one()
        self.viewed = True
        return {
            "type": "ir.actions.act_url",
            "url": self.url,
            "target": "new",
        }

    @api.model_create_multi
    def create(self, vals_list):
        video = super().create(vals_list)
        video.sync()
        return video
