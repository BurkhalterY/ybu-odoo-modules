# -*- coding: utf-8 -*-
{
    "name": "YouTube Video Chooser",
    "version": "18.0.1.0.0",
    "summary": "Your playlists into Odoo",
    "description": "Your playlists into Odoo",
    "author": "Yannis Burkhalter",
    "website": "https://github.com/BurkhalterY/ybu-odoo-addons",
    "license": "AGPL-3",
    "category": "Productivity",
    "depends": ["base_setup"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings.xml",
        "views/youtube_playlist.xml",
        "views/youtube_video.xml",
        "wizard/youtube_video_chooser.xml",
        "views/menu.xml",
    ],
    "application": True,
}
