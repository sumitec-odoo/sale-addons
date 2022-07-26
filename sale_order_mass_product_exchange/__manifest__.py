# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "sale_order_mass_product_exchange",
    "summary": "",    
    "version": "15.0.1.1.0",
    "category": "Sales",
    "website": "https://github.com/juanpgarza/sale-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
            "sale", 
            # "web_notify",
            ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_mass_product_exchange_views.xml",
        "views/sale_order_mpe_product_src_views.xml",        
        "wizards/sale_order_mass_action_view.xml",
        "views/menu_views.xml",        
    ],
}
