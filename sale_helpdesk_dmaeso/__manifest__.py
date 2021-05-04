# Copyright <2021> <David Maeso>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale - Helpdesk David Maeso",
    "version": "14.0.1.0.0",
    "author": "David Maeso, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "helpdesk_dmaeso",
    ],
    "excludes": [
        "module_name",
    ],
    "data": [
        "views/helpdesk_ticket_view.xml",
        "views/product_product_view.xml",
        "views/sale_order_view.xml",
    ],
}