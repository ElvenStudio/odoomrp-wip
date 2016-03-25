# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import fields, models, api
from openerp.addons import decimal_precision as dp


class ProductProduct(models.Model):

    _inherit = 'product.product'

    cost_price = fields.Float(
        string="Variant Cost Price", digits=dp.get_precision('Product Price'),
        groups="base.group_user", company_dependent=True)

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)

        if 'standard_price' in vals:
            res &= super(ProductProduct, self).write({'cost_price': vals['standard_price']})
        elif 'cost_price' in vals:
            res &= super(ProductProduct, self).write({'standard_price': vals['cost_price']})

        return res
