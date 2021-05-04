from odoo import fields, models, api, _

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk"
    _inherits = {'project.task': 'task_id'}

    @api.model
    def default_get(self, fields):
        defaults = super(HelpdeskTicket, self).default_get(fields)
        defaults.update({
            'project_id': self.env.ref('project_helpdesk_dmaeso.project_helpdesk').id
        })
        return defaults

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
        auto_join=True, index=True, ondelete="cascade", required=True
    )
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Describe corrective actions to do'
    )
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Describe preventive actions to do',
        translate=True
    )

    def action_assign_to_me(self):
        self.ensure_one()
        return self.task_id.action_assign_to_me()

    def action_subtask(self):
        self.ensure_one()
        return self.task_id.action_subtask()

    def action_recurring_tasks(self):
        self.ensure_one()
        return self.task_id.action_recurring_tasks()

    def _message_get_suggested_recipients(self):
        self.ensure_one
        return self.task_id._message_get_suggested_recipients()