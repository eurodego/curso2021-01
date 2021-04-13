from odoo import fields, models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk"

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    date = fields.Date(string='Fecha')