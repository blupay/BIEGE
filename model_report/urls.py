# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from model_report.views import report, report_list,report_list


urlpatterns = patterns('',
    url(r'^$', report_list, name='model_report_list'),
    url(r'^reportposition-report/$', report_list, name='model_report_list1'),
    url(r'^reportcontainer-report/$', report, name='model_report_view'),
    url(r'^(?P<slug>[\w-]+)/$', report, name='model_report_view'),
)
