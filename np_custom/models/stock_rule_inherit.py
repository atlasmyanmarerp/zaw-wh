from odoo import models, fields, api, _

class StockRuleInherit(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        """ The purpose of this method is to be override in order to easily add
        fields from procurement 'values' argument to move data.
        """
        res = super(StockRuleInherit, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        sale_line = values['sale_line_id']
        sale_line_id = self.env['sale.order.line'].sudo().search([('id', '=', sale_line)])
        if sale_line_id:
            res['restrict_partner_id'] = sale_line_id.owner_id.id
        return res

class StockMoveLineInherit(models.Model):
    _inherit = "stock.move.line"

    def _get_default_owner(self):
        for line in self:
            if line.move_id:
                line.owner_id = line.move_id.restrict_partner_id.id
    owner_id = fields.Many2one('res.partner', related='move_id.restrict_partner_id')