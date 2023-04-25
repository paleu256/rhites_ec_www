from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^user_profile_edit$', views.user_profile_edit, name='user_profile_edit'),
  
    #reports
    url(r'dashboards/reports/$', views.indexreport, name='performance_reports'),
    url(r'scorecards/reports/reports_sites_2020_to_2021\.php', views.reports_sites_2020_to_2021, name='reports_sites_2020_to_2021'),
    

    #data capture tools
    url(r'uha/gbv/qa/datacapture\.php', views.de_gbv_qaa_tool, name='de_gbv_qaa_tool'),
    url(r'uha/gbv/qa/viewdashboard\.php', views.dashboard_GbvQaaTool, name='dashboard_gbvqaatool'),
   
   
    #suplementary tools
    #TB PREV
    url(r'dashboards/prev/$', views.index, name='thematic_prev'),
    url(r'scorecards/prev/tb_prev\.php', views.tb_prev, name='prev'),
    url(r'scorecards/prev/tb_prev_summary\.php', views.tb_prev_summary, name='prev_summary'),
    
   


]
