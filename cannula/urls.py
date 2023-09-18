from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^user_profile_edit$', views.user_profile_edit, name='user_profile_edit'),
  
    #REPORTS
    url(r'dashboards/reports/$', views.indexreport, name='performance_reports'),
    
    #Quaterly section 
    url(r'scorecards/reports/quater/q_reports_sites_2022_to_2023\.asp.Net', views.q_reports_sites_2022_to_2023, name='q_reports_sites_2022_to_2023'),
    
    #Yearly section
    url(r'scorecards/reports/annual/reports_sites_2022_to_2023\.asp.Net', views.reports_sites_2022_to_2023, name='reports_sites_2022_to_2023'),

    #TESTING HOW STAFF WORKS
    #SPLIT FORM
    url(r'urc/testdataform/split/demo/gbv\.asp.net', views.testsplitform, name='testsplitform'),

    #DATA CAPTURE TOOLS

    #Demographic Details  
    url(r'urc/uha/de/demo-district/form\.asp.Net', views.getdemodistrict, name='getdemodistrict'),
    url(r'urc/uha/de/demo-healthfacility/form\.asp.Net', views.getdemohealthfacility, name='getdemohealthfacility'),
    url(r'urc/uha/de/demo-subcounty/form\.asp.Net', views.getdemosubcounty, name='getdemosubcounty'),
    
    
    
    #GBV
    url(r'uha/gbv/da/form\.asp.Net', views.getdbv_qa_data, name='getdbv_qa_data'),
    url(r'uha/gbv/da/new/update/gbvqa/form\.asp.Net', views.postgbvqaData, name='postgbvqaData'),
     

    url(r'uha/gbv/qa/datacapture\.php', views.de_gbv_qaa_tool, name='de_gbv_qaa_tool'),
    url(r'uha/gbv/qa/viewdashboard\.php', views.dashboard_GbvQaaTool, name='dashboard_gbvqaatool'),
   
   
    #suplementary tools
    #TB PREV
    url(r'dashboards/prev/$', views.index, name='thematic_prev'),
    url(r'scorecards/prev/tb_prev\.php', views.tb_prev, name='prev'),
    url(r'scorecards/prev/tb_prev_summary\.php', views.tb_prev_summary, name='prev_summary'),

    #External reports
    url(r'scorecards/reports/quater/pfmtracker/regions\.asp.Net', views.dashboard_external_pfm, name='dashboard_external_pfm'),
    
   


]
