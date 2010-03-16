# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class crm_opportunity2phonecall(osv.osv_memory):
    _name = 'crm.opportunity2phonecall'
    _description = 'Opportunity to Phonecall'

    _columns = {
        'name' : fields.char('Call summary', size=64, required=True, select=1), 
        'user_id' : fields.many2one('res.users', "Assign To"), 
        'date': fields.datetime('Date' , required=True), 
        'section_id': fields.many2one('crm.case.section', 'Sales Team'), 
    }

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param fields: List of fields for default value
        @param context: A standard dictionary for contextual values

        @return : default values of fields.
        """

        opp_obj = self.pool.get('crm.opportunity')
        record_ids = context and context.get('active_ids', []) or []
        res = {}
        for opp in opp_obj.browse(cr, uid, record_ids, context=context):
            res['name'] = opp.name
            res['user_id'] = opp.user_id and opp.user_id.id or False
            res['section_id'] = opp.section_id and opp.section_id.id or False
        return res

    def action_cancel(self, cr, uid, ids, context=None):
        """
        Closes Opportunity to Phonecall form
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Opportunity to Phonecall's IDs
        @param context: A standard dictionary for contextual values
        """
        return {'type': 'ir.actions.act_window_close'}

    def action_apply(self, cr, uid, ids, context=None):
        """
        This converts Opportunity to Phonecall and opens Phonecall view
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Opportunity to Phonecall IDs
        @param context: A standard dictionary for contextual values

        @return : Dictionary value for created Opportunity form
        """
        value = {}
        record_ids = context and context.get('active_ids', []) or []

        phonecall_obj = self.pool.get('crm.phonecall')
        opp_obj = self.pool.get('crm.opportunity')
        mod_obj = self.pool.get('ir.model.data')
        result = mod_obj._get_id(cr, uid, 'crm', 'view_crm_case_phonecalls_filter')
        res = mod_obj.read(cr, uid, result, ['res_id'])

        # Select the view
        data_obj = self.pool.get('ir.model.data')
        id2 = data_obj._get_id(cr, uid, 'crm', 'crm_case_phone_tree_view')
        id3 = data_obj._get_id(cr, uid, 'crm', 'crm_case_phone_form_view')
        if id2:
            id2 = data_obj.browse(cr, uid, id2, context=context).res_id
        if id3:
            id3 = data_obj.browse(cr, uid, id3, context=context).res_id

        for this in self.browse(cr, uid, ids, context=context):
            for opp in opp_obj.browse(cr, uid, record_ids, context=context):
                new_case = phonecall_obj.create(cr, uid, {
                        'name' : opp.name, 
                        'case_id' : opp.id , 
                        'user_id' : this.user_id and this.user_id.id or False, 
                        'categ_id' : opp.categ_id and opp.categ_id.id or False, 
                        'description' : opp.description or False, 
                        'date' : this.date, 
                        'section_id' : opp.section_id and opp.section_id.id or False, 
                        'partner_id': opp.partner_id and opp.partner_id.id or False, 
                        'partner_address_id': opp.partner_address_id and opp.partner_address_id.id or False, 
                        'partner_phone' : opp.phone or (opp.partner_address_id and opp.partner_address_id.phone or False), 
                        'partner_mobile' : opp.partner_address_id and opp.partner_address_id.mobile or False, 
                        'priority': opp.priority, 
                        'opp_id': opp.id
                }, context=context)

                phonecall_obj.case_open(cr, uid, [new_case])

            value = {
                'name': _('Phone Call'), 
                'view_type': 'form', 
                'view_mode': 'tree,form', 
                'res_model': 'crm.phonecall', 
                'res_id' : new_case, 
                'views': [(id3, 'form'), (id2, 'tree'), (False, 'calendar'), (False, 'graph')], 
                'type': 'ir.actions.act_window', 
                'search_view_id': res['res_id']
            }
        return value

crm_opportunity2phonecall()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
