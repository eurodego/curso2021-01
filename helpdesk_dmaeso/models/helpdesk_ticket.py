from odoo import fields, models, api

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = "Action"

    name = fields.Char()
    date = fields.Date()
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket')
    
class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Tag'

    name = fields.Char()
    public = fields.Boolean()
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        relation='helpdesk_ticket_tag_rel',
        column1='tag_id',
        column2='ticket_id',
        string='Tickets')
    

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

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to')
    
    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions')
    
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        relation='helpdesk_ticket_tag_rel',
        column1='ticket_id',
        column2='tag_id',
        string='Tags')
    

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

    #Calcular asignado si existe User Id en el ticket
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False

    #Cálculo de la cantidad de Tickets
    #Defino una variable entera dentro del modelo para que contenga el número de tickets
    ticket_qty = fields.Integer(
        string='Ticket Qty',
        compute='_compute_ticket_qty'
    )

    #Método que calcula el número de tickets por usuario
    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for record in self:
            other_tickets = self.env['helpdesk.ticket'].search([('user_id','=',record.user_id.id)])
            record.ticket_qty = len(other_tickets)

    #Creación del campo etiqueta. El valor que introduzca en este campo el usuario será
    #el usado para crear la nueva etiqueta.
    tag_name = fields.Char(string='Tag Name')

    def create_tag(self):
        #Actualiza solo el registro actual
        self.ensure_one()
        self.write(
            {'tag_ids': [(0,0,{'name': self.tag_name})]}
        )
        #Una vez creada la etiqueta se pone el campo en blanco para una nueva etiqueta
        self.tag_name=False