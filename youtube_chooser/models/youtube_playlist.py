import requests
from odoo import api, fields, models
from odoo.addons.youtube_chooser.utils.utils import get_channel_id


class YoutubePlaylist(models.Model):
    _name = "youtube.playlist"
    _description = "YouTube PlayList/Channel"
    _order = "name"

    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.uid
    )
    name = fields.Char("Name")
    url = fields.Char("URL")
    ttype = fields.Selection(
        [
            ("playlist", "Playlist"),
            ("channel", "Channel"),
        ],
        string="Type",
        compute="_compute_type_and_youtubeid",
    )
    youtubeid = fields.Char("YouTube ID", compute="_compute_type_and_youtubeid")

    video_ids = fields.One2many("youtube.video", "playlist_id", string="Videos")
    tag_ids = fields.Many2many("youtube.tag", string="Tags")

    _sql_constraints = [
        (
            "uniq_youtubeid",
            "UNIQUE(user_id, youtubeid)",
            "Playlist YouTube ID must be unique.",
        ),
    ]

    def _compute_type_and_youtubeid(self):
        for playlist in self:
            if "playlist" in playlist.url and "list=" in playlist.url:
                playlist.ttype = "playlist"
                playlist.youtubeid = playlist.url.split("list=")[1].split("&")[0]
            elif "/@" in playlist.url:
                playlist.ttype = "channel"
                playlist.youtubeid = playlist.url.split("@")[1].split("/")[0]
                if not (
                    playlist.youtubeid.startswith("UC")
                    and len(playlist.youtubeid) == 24
                ):
                    playlist.youtubeid = get_channel_id(
                        playlist.youtubeid, self.env.company.youtube_api_key
                    )

    def get_name_from_api(self):
        for playlist in self:
            api_url = f"https://www.googleapis.com/youtube/v3/{playlist.ttype}s"
            params = {
                "part": "snippet",
                "id": playlist.youtubeid,
                "key": self.env.company.youtube_api_key,
            }
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                playlist.name = data["items"][0]["snippet"]["title"]

    def sync_playlist(self):
        api_url = "https://www.googleapis.com/youtube/v3/playlistItems"
        for playlist in self:
            if playlist.ttype != "playlist":
                continue

            next_page_token = None
            video_ids = []
            while True:
                params = {
                    "part": "snippet,contentDetails",
                    "playlistId": playlist.youtubeid,
                    "maxResults": 50,
                    "pageToken": next_page_token,
                    "key": self.env.company.youtube_api_key,
                }
                response = requests.get(api_url, params=params)
                if response.status_code != 200:
                    continue
                data = response.json()
                for item in data.get("items", []):
                    video_ids.append(item["snippet"]["resourceId"]["videoId"])
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break

            existing_videos = (
                self.env["youtube.video"]
                .search(
                    [
                        ("user_id", "=", self.env.uid),
                        ("youtubeid", "in", video_ids),
                    ]
                )
                .mapped("youtubeid")
            )
            self.env["youtube.video"].create(
                [
                    {
                        "user_id": self.env.uid,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "playlist_id": playlist.id,
                    }
                    for video_id in video_ids
                    if video_id not in existing_videos
                ]
            )

    def sync_channel(self):
        api_url = "https://www.googleapis.com/youtube/v3/search"
        for channel in self:
            if channel.ttype != "channel":
                continue
            next_page_token = None
            video_ids = []
            while True:
                params = {
                    "part": "snippet",
                    "channelId": channel.youtubeid,
                    "maxResults": 50,
                    "order": "date",
                    "type": "video",
                    "pageToken": next_page_token,
                    "key": self.env.company.youtube_api_key,
                }
                response = requests.get(api_url, params=params)
                if response.status_code != 200:
                    continue
                data = response.json()
                for item in data.get("items", []):
                    video_ids.append(item["id"]["videoId"])
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break

            existing_videos = (
                self.env["youtube.video"]
                .search(
                    [
                        ("user_id", "=", self.env.uid),
                        ("youtubeid", "in", video_ids),
                    ]
                )
                .mapped("youtubeid")
            )
            self.env["youtube.video"].create(
                [
                    {
                        "user_id": self.env.uid,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "playlist_id": channel.id,
                    }
                    for video_id in video_ids
                    if video_id not in existing_videos
                ]
            )

    def sync(self):
        for playlist in self:
            if playlist.ttype == "playlist":
                playlist.sync_playlist()
            elif playlist.ttype == "channel":
                playlist.sync_channel()

    @api.model_create_multi
    def create(self, vals_list):
        playlist = super().create(vals_list)
        playlist.get_name_from_api()
        playlist.sync()
        return playlist
