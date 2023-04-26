from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from django.db.models import Value, CharField
from django.db.models.functions import Substr
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse

from datetime import date,datetime,timedelta
from decimal import Decimal
from itertools import groupby, tee, chain, product
from collections import OrderedDict

import openpyxl

from . import dateutil, grabbag
from .grabbag import default_zero, default, sum_zero, all_not_none, grouper

from .models import region,district,health_facility,health_subcounty,IFASBottleneck,pmtcteid_dashboard,pmtcteid,pmtcteid_targets,DOOS,mnchandmal,RMNCHAndMalaria,Lab,LabTargets,Lab_Scorecard,TbPrevTargets,TbPrev_Scorecard,TbPrev,DataElement, OrgUnit, DataValue, ValidationRule, SourceDocument, ou_dict_from_path, ou_path_from_dict
from .forms import SourceDocumentForm, DataElementAliasForm, UserProfileForm,BottleneckInventory

from .dashboards import LegendSet

import logging

logger =logging.getLogger(__name__)

def home(request):
    context = {
        'validation_rules': ValidationRule.objects.all().values_list('id', 'name')
    }
    return render(request, 'cannula/home.html', context)

@login_required
def index(request):
    context = {
        'validation_rules': ValidationRule.objects.all().values_list('id', 'name')
    }
    return render(request, 'cannula/index.html', context)

@login_required
def user_profile_edit(request):
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib import messages

    if request.POST and 'profile_save' in request.POST:
        profile_form = UserProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated')
    else:
        # create form from current user profile data
        profile_form = UserProfileForm(instance=request.user)

    if request.POST and 'passwd_change' in request.POST:
        passwd_form = PasswordChangeForm(request.user, request.POST)
        if passwd_form.is_valid():
            passwd_form.save()
            update_session_auth_hash(request, request.user)  # stop user from having to login again
            messages.success(request, 'Your password has been changed')
    else:
        # create form from current user profile data
        passwd_form = PasswordChangeForm(request.user)

    context = {
        'profile_form': profile_form,
        'passwd_form': passwd_form,
    }
    return render(request, 'cannula/user_profile_edit.html', context)

#reports logic
@login_required
def indexreport(request):
    return render(request, 'cannula/index_reports.html')

@login_required
def reports_sites_2020_to_2021(request):
    return render(request, 'cannula/performance_summary_oct_2020–sep_2021.html')

@login_required
def de_gbv_qaa_tool(request):
    return render(request, 'cannula/de_gbv_qaa_tool.html')

def dashboard_GbvQaaTool(request):
    return render(request, 'cannula/dashboard_gbvqaatool.html')

#GBV LOGIC
def getdbv_qa_data(request):
    logger.error("in get gbvqaatool")
    template_name = 'cannula/gbvqaTool.html'
    region1 = region.objects.all()
    
    return render(request,template_name,{'region':region1})


def getdemodistrict(request):
    template_name = 'partials/district.html'

    if 'region' in request.GET:
        region_id=request.GET.get('region')  
        d=district.objects.filter(roid_id=region_id)
        context={'district':d}

        logger.error("am demo districttttttttttttttttttttttt")
        return render(request,template_name,context)
    else:
        logger.error("Retunn a toast to the user")

def getdemohealthfacility(request):
    template_name = 'partials/healthfacility.html'

    if 'district' in request.GET:
        district_id=request.GET.get('district')  
        healthFacility=health_facility.objects.filter(doid_id=district_id)
        context={'health_facility':healthFacility}

        logger.error("am demo health_facilitttttttt")
        return render(request,template_name,context)
    else:
        logger.error("Retunn a toast to the user")

def getdemosubcounty(request):
    template_name = 'partials/subcounty.html'

    if 'health_facility' in request.GET:
        health_facility_id=request.GET.get('health_facility')  
        healthSubcounty=health_subcounty.objects.filter(hfoid_id=health_facility_id)
        context={'subcounty':healthSubcounty}

        logger.error("am demo subcontyyyyyyyyyyy")
        return render(request,template_name,context)
    else:
        logger.error("Retunn a toast to the user")
       













#to be removed
#suplemetary logic
@login_required
def tb_prev(request, output_format='HTML'):
    
    prev_scorecard_data  =   []
    PERIOD_LIST = list(TbPrev.objects.all().order_by('period').values_list('period', flat=True).distinct())
    PERIOD_LIST.append("None")
    DISTRICT_LIST = list(TbPrev.objects.all().order_by('district').values_list('district', flat=True).distinct())

    #Jacob filter logic and load all content code
    if 'district' in request.GET and 'period' in request.GET:
        filter_district = request.GET.get('district')
        filter_period   = request.GET.get('period')

        if request.GET.get('district') == "" and request.GET.get('period') != "None":
            query_results = TbPrev.objects.filter(period='%s' %(request.GET.get('period')))
        elif request.GET.get('district') == "" and request.GET.get('period') == "None":
            filter_district = None
            filter_period   = None
            query_results = TbPrev.objects.all()

        else:
            query_results = TbPrev.objects.filter(district='%s' %(request.GET.get('district')), period='%s' %(request.GET.get('period')))        
    else:
        filter_district = None
        filter_period   = None
        query_results = TbPrev.objects.all()

    prev_scorecard_data =read_data_tb_prev_scorecard(query_results)

    context = {
    'prev_scorecard_data': prev_scorecard_data,
    'period_desc': filter_period,
    'period_list': PERIOD_LIST,
    'district_list': DISTRICT_LIST,
    } 
    return render(request, 'cannula/tbprev.html', context)

def read_data_tb_prev_scorecard(tb_prev_raw_data):
    prev_array  =   []
    tb_pre_targets=TbPrevTargets.objects.all()

    for i in tb_prev_raw_data:
        prev=TbPrev_Scorecard()
        prev.period=i.period
        prev.district = i.district
        prev.subcounty = i.subcounty
        prev.healthfacility = i.healthfacility
        prev.target15LessN = ((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc3n + (tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc5n)#/2
        prev.target15PlusN= ((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc4n + (tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc6n)#/2
        prev.targetFemaleN=((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc3n +(tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc4n)#/2
        prev.targetMaleN=((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc5n +(tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc6n)#/2
        prev.target6To12N=((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc2n)#/2

        prev.ArtIpt15LessN = i.tbprevc3n + i.tbprevc10n
        prev.ArtIpt15PlusN=i.tbprevc4n + i.tbprevc11n
        prev.ArtIptFemaleN= i.tbprevc2n + i.tbprevc1n + i.tbprevc5n + i.tbprevc6n +i.tbprevc7n
        prev.ArtIptMaleN= i.tbprevc9n + i.tbprevc8n + i.tbprevc12n + i.tbprevc13n +i.tbprevc14n
        prev.ArtIpt6To12N= i.tbprevc17n
        prev.ArtIptContiousN= i.tbprevc20n
        prev.ArtIptAlternativeRegimenN =i.tbprevc23n + i.tbprevc26n

        if(prev.target15LessN!=0):
            prev.Perf15LessN=(prev.ArtIpt15LessN/prev.target15LessN)*100
        if(prev.target15PlusN!=0):
            prev.Perf15PlusN=(prev.ArtIpt15PlusN/prev.target15PlusN)*100
        if(prev.targetFemaleN!=0):
            prev.PerfFemaleN=(prev.ArtIptFemaleN/prev.targetFemaleN)*100
        if(prev.targetMaleN!=0):
            prev.PerfMaleN=(prev.ArtIptMaleN/prev.targetMaleN)*100
        if(prev.target6To12N!=0):
            prev.Perf6To12N=(prev.ArtIpt6To12N/prev.target6To12N)*100
    
        #denominator
        prev.target15LessD = ((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc3d + (tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc5d)#/2
        prev.target15PlusD= ((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc4d + (tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc6d)#/2
        prev.targetFemaleD=((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc3d +(tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc4d)#/2
        prev.targetMaleD=((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc5d +(tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc6d)#/2
        prev.target6To12D=((tb_pre_targets.get(healthfacility='%s' %i.healthfacility)).tbprev_tc2d)/2

        prev.ArtIpt15LessD = i.tbprevc3d + i.tbprevc10d
        prev.ArtIpt15PlusD=i.tbprevc4d + i.tbprevc11d
        prev.ArtIptFemaleD= i.tbprevc2d + i.tbprevc1d + i.tbprevc5d + i.tbprevc6d +i.tbprevc7d
        prev.ArtIptMaleD= i.tbprevc9d + i.tbprevc8d + i.tbprevc12d + i.tbprevc13d +i.tbprevc14d
        prev.ArtIpt6To12D= i.tbprevc17d
        prev.ArtIptContiousD= i.tbprevc20d
        prev.ArtIptAlternativeRegimenD =i.tbprevc23d + i.tbprevc26d

        if(prev.target15LessD!=0):
            prev.Perf15LessD=(prev.ArtIpt15LessD/prev.target15LessD)*100
        if(prev.target15PlusD!=0):
            prev.Perf15PlusD=(prev.ArtIpt15PlusD/prev.target15PlusD)*100
        if(prev.targetFemaleD!=0):
            prev.PerfFemaleD=(prev.ArtIptFemaleD/prev.targetFemaleD)*100
        if(prev.targetMaleD!=0):
            prev.PerfMaleD=(prev.ArtIptMaleD/prev.targetMaleD)*100
        if(prev.target6To12D!=0):
            prev.Perf6To12D=(prev.ArtIpt6To12D/prev.target6To12D)*100

        if(prev.ArtIpt15LessD!=0):
            prev.OverAll15Less =(prev.ArtIpt15LessN/prev.ArtIpt15LessD)*100
        if(prev.ArtIpt15PlusD!=0):
            prev.OverAll15Plus =(prev.ArtIpt15PlusN/prev.ArtIpt15PlusD)*100
        if(prev.ArtIptFemaleD!=0):
            prev.OverAllFemale =(prev.ArtIptFemaleN/prev.ArtIptFemaleD)*100
        if(prev.ArtIptMaleD!=0):
            prev.OverAllMale =(prev.ArtIptMaleN/prev.ArtIptMaleD)*100
        if(prev.ArtIpt6To12D!=0):
            prev.OverAll6To12 =(prev.ArtIpt6To12N/prev.ArtIpt6To12D)*100
        if(prev.ArtIptContiousD!=0):
            prev.OverAllContious =(prev.ArtIptContiousN/prev.ArtIptContiousD)*100
        if(prev.ArtIptAlternativeRegimenD!=0):
            prev.OverAllternativeRegimen =(prev.ArtIptAlternativeRegimenN/prev.ArtIptAlternativeRegimenD)*100

        prev_array.append(prev)

    return prev_array

def sum_tb_prev(column1,facility):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('SELECT SUM ('+column1+') FROM cannula_tbprev where healthfacility=\''+facility+'\';')
    return int(cursor.fetchone()[0])

@login_required
def tb_prev_summary(request, output_format='HTML'):

    totalagefemale=0
    totalageMale=0
    totalsixtotwelvemonthsipt=0
    totalContinuousIPT=0
    totalAlternativeRegimen=0

    if sum_tb_prev_summary('tbprevc1d')!=0:
        totalagefemale = (sum_tb_prev_summary('tbprevc1n')/sum_tb_prev_summary('tbprevc1d'))*100
    if sum_tb_prev_summary('tbprevc8d')!=0:
        totalageMale (sum_tb_prev_summary('tbprevc8n')/sum_tb_prev_summary('tbprevc8d'))*100
    if sum_tb_prev_summary('tbprevc17d')!=0:   
        totalsixtotwelvemonthsipt=(sum_tb_prev_summary('tbprevc17n')/sum_tb_prev_summary('tbprevc17d'))*100
    if sum_tb_prev_summary('tbprevc20d')!=0:  
        totalContinuousIPT=(sum_tb_prev_summary('tbprevc20n')/sum_tb_prev_summary('tbprevc20d'))*100
    if sum_tb_prev_summary('tbprevc23d')!=0:
        totalAlternativeRegimen=(sum_tb_prev_summary('tbprevc23n')/sum_tb_prev_summary('tbprevc23d'))*100
  
    perfNagefemale=0
    perfNageMale=0
    perfNsixtotwelvemonthsipt=0
    perfNContinuousIPT=0
    perfNAlternativeRegimen=0

    if sumagedisaggregation('tbprev_tc3n','tbprev_tc4n')!=0:
        perfNagefemale = (sum_tb_prev_summary('tbprevc1n')/sumagedisaggregation('tbprev_tc3n','tbprev_tc4n'))*100
    if sumagedisaggregation('tbprev_tc5n','tbprev_tc6n')!=0:
        perfNageMale = (sum_tb_prev_summary('tbprevc8n')/sumagedisaggregation('tbprev_tc5n','tbprev_tc6n'))*100
    if singleagedisaggregation('tbprev_tc2n')!=0:
        perfNsixtotwelvemonthsipt = (sum_tb_prev_summary('tbprevc2n')/singleagedisaggregation('tbprev_tc2n'))*100


    perfDagefemale=0
    perfDageMale=0
    perfDsixtotwelvemonthsipt=0
    perfDContinuousIPT=0
    perfDAlternativeRegimen=0

    if sumagedisaggregation('tbprev_tc3d','tbprev_tc4d')!=0:
        perfNagefemale = (sum_tb_prev_summary('tbprevc1d')/sumagedisaggregation('tbprev_tc3d','tbprev_tc4d'))*100
    if sumagedisaggregation('tbprev_tc5d','tbprev_tc6d')!=0:
        perfNageMale = (sum_tb_prev_summary('tbprevc8d')/sumagedisaggregation('tbprev_tc5d','tbprev_tc6d'))*100
    if singleagedisaggregation('tbprev_tc2d')!=0:
        perfNsixtotwelvemonthsipt = (sum_tb_prev_summary('tbprevc2d')/singleagedisaggregation('tbprev_tc2d'))*100

    context = {
    't_nage15less': sumagedisaggregation('tbprev_tc3n','tbprev_tc5n'),
    't_nage15plus': sumagedisaggregation('tbprev_tc4n','tbprev_tc6n'),
    't_nagefemale': sumagedisaggregation('tbprev_tc3n','tbprev_tc4n'),
    't_nageMale': sumagedisaggregation('tbprev_tc5n','tbprev_tc6n'),
    't_nsixtotwelvemonthsipt': singleagedisaggregation('tbprev_tc2n'),
    
    'nage15less': sum_tb_prev_summary('tbprevc3n') +  sum_tb_prev_summary('tbprevc10n'),
    'nage15plus': sum_tb_prev_summary('tbprevc4n') +  sum_tb_prev_summary('tbprevc11n'),  
    'nagefemale': sum_tb_prev_summary('tbprevc1n')+  sum_tb_prev_summary('tbprevc2n')+  sum_tb_prev_summary('tbprevc5n')+  sum_tb_prev_summary('tbprevc6n')+  sum_tb_prev_summary('tbprevc7n'),
    'nageMale': sum_tb_prev_summary('tbprevc8n') +  sum_tb_prev_summary('tbprevc9n')+  sum_tb_prev_summary('tbprevc12n')+  sum_tb_prev_summary('tbprevc13n')+  sum_tb_prev_summary('tbprevc14n'),
    'nsixtotwelvemonthsipt': sum_tb_prev_summary('tbprevc17n'),
    'nContinuousIPT': sum_tb_prev_summary('tbprevc20n'),
    'nAlternativeRegimen': sum_tb_prev_summary('tbprevc23n')+sum_tb_prev_summary('tbprevc26n'),


    't_dage15less': sumagedisaggregation('tbprev_tc3d','tbprev_tc5d'),
    't_dage15plus': sumagedisaggregation('tbprev_tc4d','tbprev_tc6d'),
    't_dagefemale': sumagedisaggregation('tbprev_tc3d','tbprev_tc4d'),
    't_dageMale': sumagedisaggregation('tbprev_tc5d','tbprev_tc6d'),
    't_dsixtotwelvemonthsipt': singleagedisaggregation('tbprev_tc2d'),

    'dage15less': sum_tb_prev_summary('tbprevc3d')+  sum_tb_prev_summary('tbprevc10d'),
    'dage15plus': sum_tb_prev_summary('tbprevc4d')+  sum_tb_prev_summary('tbprevc11d'),
    'dagefemale': sum_tb_prev_summary('tbprevc1d')+  sum_tb_prev_summary('tbprevc2d')+  sum_tb_prev_summary('tbprevc5d')+  sum_tb_prev_summary('tbprevc6d')+  sum_tb_prev_summary('tbprevc7d'),
    'dageMale': sum_tb_prev_summary('tbprevc8d')+  sum_tb_prev_summary('tbprevc9n')+  sum_tb_prev_summary('tbprevc12n')+  sum_tb_prev_summary('tbprevc13n')+  sum_tb_prev_summary('tbprevc14n'),
    'dsixtotwelvemonthsipt': sum_tb_prev_summary('tbprevc17d'),
    'dContinuousIPT': sum_tb_prev_summary('tbprevc20d'),
    'dAlternativeRegimen': sum_tb_prev_summary('tbprevc23d')+sum_tb_prev_summary('tbprevc26n'),

    'totalage15less': ((sum_tb_prev_summary('tbprevc3n')+  sum_tb_prev_summary('tbprevc10n'))/(sum_tb_prev_summary('tbprevc3d')+  sum_tb_prev_summary('tbprevc10d')))*100,
    'totalage15plus': ((sum_tb_prev_summary('tbprevc4n')+  sum_tb_prev_summary('tbprevc11n'))/(sum_tb_prev_summary('tbprevc4d')+  sum_tb_prev_summary('tbprevc11d')))*100,
    'totalagefemale':totalagefemale,
    'totalageMale': totalageMale,
    'totalsixtotwelvemonthsipt': totalsixtotwelvemonthsipt,
    'totalContinuousIPT': totalContinuousIPT,
    'totalAlternativeRegimen': totalAlternativeRegimen,

    'perfNage15less': ((sum_tb_prev_summary('tbprevc3n')+  sum_tb_prev_summary('tbprevc10n'))/sumagedisaggregation('tbprev_tc3n','tbprev_tc5n'))*100,
    'perfNage15plus': ((sum_tb_prev_summary('tbprevc4n')+  sum_tb_prev_summary('tbprevc11n'))/sumagedisaggregation('tbprev_tc4n','tbprev_tc6n'))*100,
    'perfNagefemale': perfNagefemale,
    'perfNageMale': perfNageMale,
    'perfNsixtotwelvemonthsipt': perfNsixtotwelvemonthsipt,
    'perfNContinuousIPT': perfNContinuousIPT,
    'perfNAlternativeRegimen': perfNAlternativeRegimen,

    'perfDage15less': ((sum_tb_prev_summary('tbprevc3d')+  sum_tb_prev_summary('tbprevc10d'))/sumagedisaggregation('tbprev_tc3d','tbprev_tc5d'))*100,
    'perfDage15plus': ((sum_tb_prev_summary('tbprevc4d')+  sum_tb_prev_summary('tbprevc11d'))/sumagedisaggregation('tbprev_tc4d','tbprev_tc6d'))*100,
    'perfDagefemale': perfDagefemale,
    'perfDageMale': perfDageMale,
    'perfDsixtotwelvemonthsipt': perfDsixtotwelvemonthsipt,
    'perfDContinuousIPT': perfDContinuousIPT,
    'perfDAlternativeRegimen': perfDAlternativeRegimen,
    
    } 
    return render(request, 'cannula/tbprev_summary.html', context)

def sumagedisaggregation(column1,column2):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('SELECT SUM ('+column1+') FROM cannula_tbprevtargets;')

    cursor1 = connection.cursor()
    cursor1.execute('SELECT SUM ('+column2+') FROM cannula_tbprevtargets;')
   
    return (int(cursor.fetchone()[0]) + int(cursor1.fetchone()[0]))

def singleagedisaggregation(column1):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('SELECT SUM ('+column1+') FROM cannula_tbprevtargets;')

    return int(cursor.fetchone()[0])

def sum_tb_prev_summary(column1):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('SELECT SUM ('+column1+') FROM cannula_tbprev;')

    return int(cursor.fetchone()[0])

