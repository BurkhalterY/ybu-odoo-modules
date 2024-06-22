# -*- coding: utf-8 -*-
{
    "name": "Foosball",
    "version": "17.0.0.2.0",
    "description": """Keep track of your matches! ⚽""",
    "author": "Yannis Burkhalter",
    "website": "https://github.com/BurkhalterY/ybu-odoo-addons/tree/17.0/foosball",
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
