from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

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
    
    @api.model
    def cron_delete_tag(self):
        tickets = self.search([('ticket_ids', '=', False)])
        tickets.unlink()

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk"

    def _date_default_today(self):
        return fields.Date.today()

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(
        string='Date',
        default=_date_default_today)

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
        string='Assigned to',
        default=lambda self: self.env.user.id)
    
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
        # Comentado por creación de etiqueta mediante botón pasando los valores por contexto tarea T06
        # self.write(
        #    {'tag_ids': [(0,0,{'name': self.tag_name})]}
        #)
        #Una vez creada la etiqueta se pone el campo en blanco para una nueva etiqueta
        #self.tag_name=False
        
        # T06-04. Modificar el botón de crear una etiqueta en el formulario de ticket para que abra una acción nueva, 
        # pasando por contexto el valor del nombre y la relación con el ticket.
        # Creo una acción llamada action_new_tag que se definirá en la view helpedesk_tag_view
        action = self.env.ref('helpdesk_dmaeso.action_new_tag').read()[0]
        action['context'] = {
            'default_name': self.tag_name,
            'default_ticket_ids': [(6,0,self.ids)]
        }
        self.tag_name = False
        return action

    #Condición para que el campo time no pueda ser menor que cero
    @api.constrains('time')
    def _time_positive(self):
        for ticket in self:
            if ticket.time and ticket.time < 0:
                raise ValidationError(_("The time no must be negative."))

    #Actualización de date_limit al cambiar la fecha del ticket
    @api.onchange('date')
    def _onchange_date(self):
        self.date_limit = self.date and self.date + timedelta(days=1)
