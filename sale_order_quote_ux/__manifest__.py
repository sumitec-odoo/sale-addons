# Copyright 2021 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "sale_order_quote_ux",
    "summary": "",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/juanpgarza/sale-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": ["sale",
                # "account",
            ],
    "data": [
        'views/sale_portal_templates.xml',
        'security/sale_order_quote_security.xml',
        ],
    "installable": True,
}