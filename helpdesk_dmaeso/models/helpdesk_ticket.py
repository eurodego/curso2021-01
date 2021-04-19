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
        help='Describe preventive actions to do',
        translate=True)

    def asignar(self):
        self.ensure_one()
        self.write({
            'state': 'asignado',
            'assigned': True
        })
    
    def proceso(self):
        self.ensure_one()
        self.write({
            'state': 'proceso'
        })
    
    # Pendiente, visible sólo con estado = en proceso o asignado
    def pendiente(self):
        self.ensure_one()
        self.write({
            'state': 'pendiente'
        })
    # Finalizar, visible en cualquier estado, menos cancelado y finalizado
    def resuelto(self):
        self.ensure_one()
        self.write({
            'state': 'resuelto'
        })
    # Cancelar, visible si no está cancelado
    def cancelar(self):
        self.ensure_one()
        self.write({
            'state': 'cancelado'
        })