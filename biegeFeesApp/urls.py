from django.conf.urls.defaults import *
from biegeFeesApp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from model_report import report
report.autodiscover()
urlpatterns = patterns('',
                  # school details
		  url(r'^$', 'biegeFeesApp.views.do_login'),
		  url(r'^school/dashboard/$', 'biegeFeesApp.views.dashboard'),
		  url(r'^school/register/$', 'biegeFeesApp.views.register'),
                  url(r'^school/records/$', 'biegeFeesApp.views.student_records'),
                  url(r'^school/sch-search/(?P<term>.*?)$','biegeFeesApp.views.stud_search_id'),
                  url(r'^school/search_surname/(?P<term>.*?)$','biegeFeesApp.views.stud_search_surname'),
                  url(r'^school/fees/$', 'biegeFeesApp.views.fees_setup'),

                  #beige details
		  url(r'^login/$', 'biegeFeesApp.views.beige_login'),
		  url(r'^beige/dashboard/$', 'biegeFeesApp.views.beige_dashboard',name = 'monitor-test'),
		  #url(r'^payment/$', 'biegeFeesApp.views.beige_payment'),
		  
		  url(r'^monitor/$', 'biegeFeesApp.views.monitor', name = 'monitor' ),
		  
		  
		  url(r'^school_reg/$', 'biegeFeesApp.views.school_reg'),
		  url(r'^add_school_user/$', 'biegeFeesApp.views.adduser_sch'),
                  url(r'^add_beige_user/$', 'biegeFeesApp.views.adduser_beige'),
                  
		  url(r'^school_details/(?P<term>.*?)/(?P<showDetails>.*?)/$', 'biegeFeesApp.views.school_detail'),
		  
                  url(r'^st_search/(?P<term>.*?)$','biegeFeesApp.views.student_search_beige'),
                  url(r'^walk_in/$', 'biegeFeesApp.views.walk_in'),
                  url(r'^teller/report/$', 'biegeFeesApp.views.teller_report'),
                  url(r'^search/$', search, name = 'search' ),
                  url(r'^sch/search/(?P<term>.*?)$','biegeFeesApp.views.sch_search' ),
		  url(r'^teller/details/(?P<term>.*?)/(?P<showDetails>.*?)/$', 'biegeFeesApp.views.teller_details'),
                  
			# Transaction Urls
                  url(r'^st-search/(?P<term>.*?)$','biegeFeesApp.views.student_search'),
                  url(r'^std_details/(?P<term>.*?)/(?P<showDetails>.*?)/$', 'biegeFeesApp.views.payment_detail'),
 		  url(r'^st_details/(?P<term>.*?)/(?P<showDetails>.*?)/$', 'biegeFeesApp.views.student_detail'),
                  url(r'^payment/$', 'biegeFeesApp.views.payment'),
                  url(r'^print/(?P<term>.*?)/(?P<showDetails>.*?)/$', 'biegeFeesApp.views.print_trans'),

			#beige Change Password
		  url(r'^changepass/$','biegeFeesApp.views.password_change'),

			#School Change Password
		  url(r'^school/changepass/$','biegeFeesApp.views.school_password_change'),
		  url(r'^logout/$', 'biegeFeesApp.views.do_logout'),
                  url(r'^school/logout/$', 'biegeFeesApp.views.do_logouT'),


		  #url(r'^beige/changedpass/$','biegeFeesApp.views.changedpass'),

		  #url(r'^$', 'biegeFeesApp.views.do_logout'),

		  #url(r'^aics/changepass/$','aics_urls.views.password_change'),
		  #url(r'^aics/changedpass/$','aics_urls.views.changedpass'),
		  #url(r'^logout/$', 'aics_urls.views.do_logout'),
		  
		  #CREW URLS
		  #url(r'^crew/$', 'aics_urls.views.crew'),
		  #url(r'^crew/search/(?P<term>.*?)$','aics_urls.views.crew_search'),
		  #url(r'^crew/list/$', 'aics_urls.views.crew_list'),
		  #url(r'^crew_details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.crew_detail'),
		 
		  
		 
		  
)

urlpatterns += staticfiles_urlpatterns()
