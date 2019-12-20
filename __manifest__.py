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

{
    'name': 'Employee Complaints',
    'version': '0.3',
    'author': 'One Click Software',
    'category': 'Human Resources',
    'website': 'http://oneclick.solutions',
    'summary': 'Performance Management, Complaints,',
    'depends': ['hr', 'mail', 'calendar'],
    'description': """
Employee Complaint Record
==========================
Creates forms and reports for reporting complaints against employees
""",
    "data": [
        'views/hr_complaint_view.xml',
        'report/hr_complaint_report.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
