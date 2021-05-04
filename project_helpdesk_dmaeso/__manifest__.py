# Copyright <2021> <David Maeso>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project Helpdesk David Maeso",
    "version": "14.0.1.0.0",
    "author": "David Maeso, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "project",
    ],
    "excludes": [
        "module_name",
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "views/helpdesk_menu.xml",
        "views/helpdesk_view.xml",
        "data/project_helpdesk_data.xml",
    ],
}