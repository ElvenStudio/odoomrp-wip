# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.one
    def merge_stock_quants(self):
        if not self.reservation_id:
            quants = self.search(
                [('id', '!=', self.id),
                 ('product_id', '=', self.product_id.id),
                 ('lot_id', '=', self.lot_id.id),
                 ('package_id', '=', self.package_id.id),
                 ('location_id', '=', self.location_id.id),
                 ('reservation_id', '=', False),
                 ('propagated_from_id', '=', False)])
            qty = cost = 0
            for quant in quants:
                qty += quant.qty
                cost += quant.cost
                quant.unlink()
            self.cost += cost
            self.qty += qty

    @api.model
    def quants_unreserve(self, move):
        related_quants = [x for x in move.reserved_quant_ids]
        super(StockQuant, self).quants_unreserve(move)
        for quant in related_quants:
            quant.merge_stock_quants()
