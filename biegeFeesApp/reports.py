from models import *
from model_report.report import reports, ReportAdmin
from django.utils.translation import ugettext_lazy as _
from model_report.utils import (usd_format, avg_column, sum_column, count_column)

def amount_format(value,instance):
      rvalue = int(value)
      return _('%s' %rvalue)
      
def sch_format(value,instance):
      return _('%s' %value)

def school_label(report, field):
    return _("Schools")
    
def fee_label(report, field):
    return _("Fees Type")

def date_label(report, field):
    return _("Date")
    
def teller_label(report, field):
    return _("Teller")
    
def filter_school(report, values):
    return _('%s' %values)
    
    
class Trans_Report(ReportAdmin):
	title=('Transactions')
	model= BeigeTransaction
	fields = ['studentID__surname','studentID__othername','studentID__schoolID__schoolName','feesType__name','amount','date_added','tellerID__branch__branch_name','tellerID__username',]
	list_order_by = ('-date_added',)
	list_group_by = ('date_added','tellerID__branch__branch_name','tellerID','studentID__schoolID__schoolName',)
	list_filter = ('date_added','tellerID__branch__branch_name',)

	type = 'chart'

	group_totals = {
        'amount': sum_column,
	
	}
	report_totals={
	'amount':sum_column,
	}
	
	override_field_formats = {
        #'studentID__schoolID__schoolName':sch_format,	
	}
	override_field_labels ={
	#'studentID__schoolID__schoolName':school_label,
	'feesType__name':fee_label,
	'tellerID__username':teller_label,
	'date_added':date_label,
	}
	override_field_filter_values = {
        #'studentID__schoolID__schoolName': filter_school
    	}
    	override_field_choices = {
        #'studentID__schoolID__schoolName': filter_school
      	}
	
	list_serie_fields = ('amount',)

	chart_types = ('pie', 'column', 'line')

reports.register('transactions-report',Trans_Report)



