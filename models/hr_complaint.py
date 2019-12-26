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

from datetime import date

from odoo import api, fields, models
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF

class HrComplaint(models.Model):
	_name = "hr_complaint.complaint"
	_description = "Employee Complaint"
	_inherit = "mail.thread"
			
	name = fields.Char("Name")
	complaint_date = fields.Date("Date of Complaint", required=True, default=date.today())
	employee_id = fields.Many2one('hr.employee', "Employee", required=True)
	complaint_mode = fields.Selection([
            ('0', 'Telephone'),
            ('1', 'Other Verbal'),
            ('2', 'In writing')], "Method of Complaint", help="This is the mode by which the complaint was received.")
	complaint_type = fields.Selection([
            ('0', 'Formal'),
            ('1', 'Informal')], "Type of Complaint")
	complaint_source = fields.Selection([
            ('0', 'Client'),
            ('1', 'Public'),
	    ('2', 'Other Employee'),
	    ('3', 'Management')], "Source of Complaint")
	complaint_source_text = fields.Char('Complainant',size=100)
	complaint_outline = fields.Text('Outline of Complaint')
	complaint_evidence = fields.Text('Evidence')
	complaint_witnesses = fields.Text('Witnesses')
	recorded_by = fields.Many2one('hr.employee',"Complaint Recorded By",required=True)
	complaint_assessment = fields.Selection([
            ('0', 'Trivial'),
            ('1', 'Minor'),
	    ('2', 'Moderate'),
	    ('3', 'Serious'),
	    ('4', 'Very Serious')], "Seriousness of complaint")
#allegations questions
	stealing = fields.Boolean('Stealing')
	fraud = fields.Boolean('Fraud')
	violence = fields.Boolean('Threats and/or violence')
	safety = fields.Boolean('Safety breaches')
	discrimination = fields.Boolean('Discrimination')
#indicator question
	policy = fields.Boolean('Breach of contract/policy')
	client_contract = fields.Boolean('Breach of the company\'s contracts with clients')
	directions = fields.Boolean('Refusal to follow reasonable directions')
	performance = fields.Boolean('Unsatisfactory performance')
	behaviour = fields.Boolean('Inappropriate behaviour')
	property = fields.Boolean('Misuse of company property')
	evidence_sufficient = fields.Boolean('Is there sufficient evidence to investigate?')
	investigation_required =fields.Selection([
	    ('1', 'Yes - Formal'),
	    ('2', 'Yes - Informal'),
	    ('3', 'No')], 'Does the complaint require investigation?')
	complaint_refer = fields.Boolean('Does the complaint have to be referred to another organisation?')
	investigation_plan = fields.Text('Investigation methods/plan')
	assigned_to = fields.Many2one('hr.employee',"Investigator")
	assessor = fields.Many2one('hr.employee',"Assessor")
	assess_date = fields.Date('Assessment Completed')
	substantiated = fields.Boolean('Has the complaint been substantitated?')
	action_detail = fields.Text('Details')
	issues = fields.Text('Issues discovered')
	action_taken = fields.Selection([
	    ('1', 'Disciplinary Action'),
	    ('2', 'Formal Warning'),
	    ('3', 'Informal Warning'),
	    ('4', 'Record without warning'),
	    ('5', 'Remedial'),
	    ('6', 'No action')], 'Action to be taken', track_visibility='onchange')
	record_employee = fields.Boolean('Record on employee file', track_visibility='onchange')
	notes = fields.Text('Notes', track_visibility='onchange')
	completed_by = fields.Many2one('hr.employee','Completed By')
	state = fields.Selection([
            ('draft', 'New'),
            ('insufficient', 'Insufficient Evidence'),
            ('progress', 'Investigation in progress'),
            ('wait', 'Waiting for external investigation'),
            ('unsubstantiated','Unsubstantiated'),
            ('done', 'Done')], 'Status', required=True, readonly=True, track_visibility='onchange', copy=False, default='draft')
	date_eta = fields.Date('To be completed')
	date_close = fields.Date('Date closed')
    
	@api.onchange('employee_id','complaint_date')
	def change_complaint(self):
		if self.employee_id:
			self.name = self.employee_id.name
		else:
			self.name = ''
		if self.complaint_date:
			self.name += ' (' + str(self.complaint_date) + ')'
			
	_order = 'complaint_date desc'

class HrEmployee(models.Model):
	_inherit="hr.employee"
	
	complaint_count = fields.Integer(compute='_compute_ccount', store=False, string='Complaints')
	
	@api.multi
	def _compute_ccount(self):
		Complaint = self.env['hr_complaint.complaint']
		self.complaint_count = Complaint.search_count([('employee_id','=',self.id)])
