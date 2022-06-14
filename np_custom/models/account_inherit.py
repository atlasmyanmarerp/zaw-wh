from odoo import models, fields, api, _

class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    owner_id = fields.Many2one('res.partner', string="Owner")
    weight = fields.Integer(string="Weight")
    weight_uom = fields.Many2one('uom.uom', string="Weight UoM")