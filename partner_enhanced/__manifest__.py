# -*- coding: utf-8 -*-
{
    "name": "Partner Enhanced",
    "version": "17.0.0.1.0",
    "description": """
Add some useful fields on partners:
- Many phones, emails and websites
- Firstname & lastname, but without display name
- Birthday
- Gender
- Additional names
""",
    "author": "Yannis Burkhalter",
    "website": "https://github.com/BurkhalterY/ybu-odoo-addons/tree/17.0/partner_enhanced",
    "license": "AGPL-3",
    "category": "Productivity",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/res_partner_data.xml",
    ],
    "post_init_hook": "post_init_hook",
}
