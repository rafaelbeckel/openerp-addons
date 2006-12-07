# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id: account.py 1005 2005-07-25 08:41:42Z nicoe $
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import time
import netsvc
from osv import fields, osv
import ir

class purchase_order(osv.osv):
	def _amount_untaxed(self, cr, uid, ids, prop, unknow_none,unknow_dict):
		ti = []
		for inv in self.read(cr, uid, ids, ['price_type']):
			if inv['price_type']=='tax_included':
				ti.append(inv['id'])
		id_set=",".join(map(str,ids))
		cr.execute("SELECT s.id,COALESCE(SUM(l.price_unit*l.product_qty),0)::decimal(16,2) AS amount FROM purchase_order s LEFT OUTER JOIN purchase_order_line l ON (s.id=l.order_id) WHERE s.id IN ("+id_set+") GROUP BY s.id ")
		res=dict(cr.fetchall())
		if len(ti):
			tax = self._amount_tax(cr, uid, ti, prop, unknow_none,unknow_dict)
			for id in ti:
				res[id] = res[id] - tax.get(id, 0.0)
		return res

	def _amount_tax(self, cr, uid, ids, field_name, arg, context):
		res = {}
		for order in self.browse(cr, uid, ids):
			val = 0.0
			for line in order.order_line:
				for tax in line.taxes_id:
					if order.price_type=='tax_included':
						ttt = self.pool.get('account.tax').compute_inv(cr, uid, [tax.id], line.price_unit, line.product_qty, order.partner_address_id.id)
					else:
						ttt = self.pool.get('account.tax').compute(cr, uid, [tax.id], line.price_unit, line.product_qty, order.partner_address_id.id)
					for c in ttt:
						val += round(c['amount'], 2)
			res[order.id]=round(val,2)
		return res
	_inherit = "purchase.order"
	_columns = {
		'price_type': fields.selection([
			('tax_included','Tax included'),
			('tax_excluded','Tax excluded')
		], 'Price method', required=True),
		'amount_untaxed': fields.function(_amount_untaxed, method=True, string='Untaxed Amount'),
		'amount_tax': fields.function(_amount_tax, method=True, string='Taxes'),
	}
	_defaults = {
		'price_type': lambda *a: 'tax_excluded',
	}
	def _inv_get(self, cr, uid, order, context={}):
		return {
			'price_type': order.price_type
		}
purchase_order()

