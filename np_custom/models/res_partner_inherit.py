from email.policy import default
from odoo import models, fields, api

class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    owner_status = fields.Boolean(string = "Owner Status", default=False)