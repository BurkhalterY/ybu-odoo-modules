# -*- coding: utf-8 -*-
{
    "name": "Foosball",
    "version": "16.0.0.1.0",
    "description": """Keep track of your matches! ⚽""",
    "author": "Yannis Burkhalter",
    "website": "https://github.com/BurkhalterY/ybu-odoo-addons/tree/16.0/foosball",
    "license": "AGPL-3",
    "category": "Productivity",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/foosball_match.xml",
        "views/menu.xml",
    ],
    "application": True,
}
