from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def _compute_owner_status(self, product_id, order_id):
        partner_id = self.env['res.partner'].sudo().search([])
        for partner in partner_id:
            quant_id = self.env['stock.quant'].sudo().search([
                ('owner_id', '=', partner.id),
                ('product_id', '=', product_id.id),
                ('location_id', '=', order_id.warehouse_id.lot_stock_id.id)
            ])
            if quant_id:
                for res in quant_id:
                    if res.available_quantity > 0:
                        partner.owner_status = True
                    else:
                        partner.owner_status = False
            else:
                partner.owner_status = False

    @api.onchange('product_id', 'warehouse_id')
    def _get_partner_domain(self):
        print("Here")
        for line in self:
            if line.product_id:
                line._compute_owner_status(line.product_id, line.order_id)
                line.owner_id = False
                # return [('owner_status', '=', True)]
                return {'domain':{'owner_id':[('owner_status','=',True)]}}
            else:
                return False

    @api.onchange('owner_id', 'product_id', 'warehouse_id')
    def _get_balance_qty(self):
        for line in self:
            if line.owner_id:
                quant_id = self.env['stock.quant'].sudo().search([
                    ('owner_id', '=', line.owner_id.id),
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.order_id.warehouse_id.lot_stock_id.id)
                ])
                line.available_qty = quant_id.available_quantity
            else:
                line.available_qty = 0

    @api.onchange('product_uom_qty', 'owner_id')
    def _onchange_uom_qty(self):
        for line in self:
            if line.owner_id:
                if line.product_uom_qty > line.available_qty:
                    raise UserError(_("Quantity is more than owner available quantity."))

    owner_id = fields.Many2one(
        'res.partner',
        domain="[('owner_status', '=', True)]"
    )
    weight = fields.Integer(string="Weight")
    weight_uom = fields.Many2one('uom.uom', string="Weight UoM")
    available_qty = fields.Float(string="Balance Qty", compute=_get_balance_qty)

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        self.ensure_one()
        res.update({"owner_id": self.owner_id.id})   
        res.update({"weight": self.weight})
        res.update({"weight_uom": self.weight_uom.id})
        return res

