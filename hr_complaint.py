# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser
import time

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF

class hr_complaint(osv.Model):
    _name = "hr_complaint.complaint"
    _description = "Employee Complaint"
    _inherit = "mail.thread"
    
    def onchange_complaint(self, cr, uid, ids, employee, date):
		res = {}
		if employee:
			employee_obj = self.pool.get('hr.employee').browse(cr, uid, employee)
			res['name'] = employee_obj.name
		else:
			res['name'] = ''
		if date:
			res['name'] += ' (' + str(date) + ')'
		
		return {'value': res}
    
    _columns = {
		'name': fields.char("Name"),
        'complaint_date': fields.date("Date of Complaint", required=True, select=True),
        'employee_id': fields.many2one('hr.employee', "Employee", required=True),
	'complaint_mode': fields.selection([
            ('0', 'Telephone'),
            ('1', 'Other Verbal'),
            ('2', 'In writing')], "Method of Complaint", help="This is the mode by which the complaint was received."),
	'complaint_type': fields.selection([
            ('0', 'Formal'),
            ('1', 'Informal')], "Type of Complaint"),
	'complaint_source': fields.selection([
            ('0', 'Client'),
            ('1', 'Public'),
	    ('2', 'Other Employee'),
	    ('3', 'Management')], "Source of Complaint"),
	'complaint_source_text': fields.char('Complainant',size=100),
        'complaint_outline': fields.text('Outline of Complaint'),
	'complaint_evidence': fields.text('Evidence'),
	'complaint_witnesses': fields.text('Witnesses'),
	'recorded_by': fields.many2one('hr.employee',"Complaint Recorded By",required=True),
	'complaint_assessment': fields.selection([
            ('0', 'Trivial'),
            ('1', 'Minor'),
	    ('2', 'Moderate'),
	    ('3', 'Serious'),
	    ('4', 'Very Serious')], "Seriousness of complaint"),
#allegations questions
	'stealing': fields.boolean('Stealing'),
	'fraud': fields.boolean('Fraud'),
	'violence': fields.boolean('Threats and/or violence'),
	'safety': fields.boolean('Safety breaches'),
	'discrimination': fields.boolean('Discrimination'),
#indicator question
	'policy': fields.boolean('Breach of contract/policy'),
	'client_contract': fields.boolean('Breach of the company\'s contracts with clients'),
	'directions': fields.boolean('Refusal to follow reasonable directions'),
	'performance': fields.boolean('Unsatisfactory performance'),
	'behaviour': fields.boolean('Inappropriate behaviour'),
	'property': fields.boolean('Misuse of company property'),

	'evidence_sufficient': fields.boolean('Is there sufficient evidence to investigate?'),
	'investigation_required':fields.selection([
	    ('1', 'Yes - Formal'),
	    ('2', 'Yes - Informal'),
	    ('3', 'No')], 'Does the complaint require investigation?'),
	'complaint_refer': fields.boolean('Does the complaint have to be referred to another organisation?'),
	'investigation_plan': fields.text('Investigation methods/plan'),
	'assigned_to': fields.many2one('hr.employee',"Investigator"),
	'assessor': fields.many2one('hr.employee',"Assessor"),
	'assess_date': fields.date('Assessment Completed'),
	'substantiated': fields.boolean('Has the complaint been substantitated?'),
	'action_detail': fields.text('Details'),
	'issues': fields.text('Issues discovered'),
	'action_taken': fields.selection([
	    ('1', 'Disciplinary Action'),
	    ('2', 'Formal Warning'),
	    ('3', 'Informal Warning'),
	    ('4', 'Record without warning'),
	    ('5', 'Remedial'),
	    ('6', 'No action')], 'Action to be taken', track_visibility='onchange'),
	'record_employee': fields.boolean('Record on employee file', track_visibility='onchange'),
	'notes': fields.text('Notes', track_visibility='onchange'),
	'completed_by': fields.many2one('hr.employee','Completed By'),
        'state': fields.selection([
            ('draft', 'New'),
            ('insufficient', 'Insufficient Evidence'),
            ('progress', 'Investigation in progress'),
            ('wait', 'Waiting for external investigation'),
            ('unsubstantiated','Unsubstantiated'),
            ('done', 'Done')], 'Status', required=True, readonly=True, track_visibility='onchange', copy=False),
	'date_eta': fields.date('To be completed'),
    'date_close': fields.date('Date closed', select=True),
    }
    _defaults = {
        'date': lambda *a: (parser.parse(datetime.now().strftime('%Y-%m-%d')) + relativedelta(months=+1)).strftime('%Y-%m-%d'),
        'state': lambda *a: 'draft',
    }
    
    _order = 'complaint_date desc'

class hr_employee(osv.Model):
    _name = "hr.employee"
    _inherit="hr.employee"
    
    def _complaint_count(self, cr, uid, ids, field_name, arg, context=None):
        Complaint = self.pool['hr_complaint.complaint']
        return {
            employee_id: Complaint.search_count(cr, uid, [('employee_id', '=', employee_id)], context=context)
            for employee_id in ids
        }

    _columns = {
         'complaint_count': fields.function(_complaint_count, type='integer', string='Complaints'),
    }
