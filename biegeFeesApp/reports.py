from models import *
from model_report.report import reports, ReportAdmin
from django.utils.translation import ugettext_lazy as _
from model_report.utils import (usd_format, avg_column, sum_column, count_column)

def amount_format(value,instance):
      rvalue = int(value)
      return _('%s' %rvalue)




class Trans_Report(ReportAdmin):
	title=('Transactions')
	model= BeigeTransaction
	fields = ['studentID__surname','studentID__othername','studentID__schoolID__schoolName','feesType__name','amount','date_added','tellerID',]
	#list_order_by = ('surname',)
	list_group_by = ('date_added','tellerID','studentID__schoolID__schoolName',)
	list_filter = ('date_added','studentID__schoolID__schoolName',)

	type = 'report'

	group_totals = {
        'amount': sum_column,
	
	}
	override_field_formats ={
	'amount':amount_format,
	}
	list_serie_fields = ('amount',)

	chart_types = ('pie', 'column', 'line')

reports.register('transactions-report',Trans_Report)



