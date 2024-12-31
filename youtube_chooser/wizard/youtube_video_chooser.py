import random

from odoo import fields, models


class YoutubeVideoChooser(models.TransientModel):
    _name = "youtube.video.chooser"
    _description = "YouTube Video Chooser"

    tag_ids = fields.Many2many("youtube.tag", string="Tags")

    def action_random(self):
        domain = [("user_id", "=", self.env.uid), ("viewed", "=", False)]
        if self.tag_ids:
            domain += [
                "|",
                ("tag_ids", "in", self.tag_ids.ids),
                ("playlist_id.tag_ids", "in", self.tag_ids.ids),
            ]
        videos = self.env["youtube.video"].search(domain)
        if not videos:
            return
        video = random.choice(videos)
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "youtube.video",
            "res_id": video.id,
        }
