import random

from odoo import fields, models


class YoutubeVideoChooser(models.TransientModel):
    _name = "youtube.video.chooser"
    _description = "YouTube Video Chooser"

    tag_ids = fields.Many2many("youtube.tag", string="Tags")
    duration_min = fields.Float("Min. Duration")
    duration_max = fields.Float("Max. Duration")
    lang_id = fields.Many2one("res.lang", string="Language")

    def action_random(self):
        domain = [("user_id", "=", self.env.uid), ("viewed", "=", False)]
        if self.tag_ids:
            domain += [
                "|",
                ("tag_ids", "in", self.tag_ids.ids),
                ("playlist_id.tag_ids", "in", self.tag_ids.ids),
            ]
        if self.duration_min:
            domain.append(("duration", ">=", self.duration_min))
        if self.duration_max:
            domain.append(("duration", "<=", self.duration_max))
        if self.lang_id:
            domain.append(("lang_id", "=", self.lang_id))
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
