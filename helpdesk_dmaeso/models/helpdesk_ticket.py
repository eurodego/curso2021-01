from odoo import fields, models

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')

    state = fields.Selection(
        [('nuevo','Nuevo'),
        ('asignado', 'Asignado'),
        ('proceso','En proceso'),
        ('pendiente','Pendiente'),
        ('resuelto','Resuelto'),
        ('cancelado', 'Cancelado')],
        string='State',
        default='nuevo')

    time = fields.Float(string='Time')

    assigned = fields.Boolean(string='Assigned', readonly=True)

    date_limit = fields.Date(string='Date Limit')

    action_corrective = fields.Html(
        string='Corrective Action',
        help='Describe corrective actions to do')

    action_preventive = fields.Html(
        string='Preventive Action',
        help='Describe preventive actions to do')

