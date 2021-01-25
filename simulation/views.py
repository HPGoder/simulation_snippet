from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from projects.models import project,AcceptanceCriteria, weld_configuration, aut_indications ,PlanarIndicationAcceptanceCriteria_load, PlanarIndicationAcceptanceCriteria, ConcavitySaggingCriteria, PorosityCriteria, ClusterPorosityCriteria, SlagCriteria, Other1Criteria, Other2Criteria, Other3Criteria, Other4Criteria, Other5Criteria
from projects.forms import WeldConfig_form
from .filters import ECAfilter, WeldConfigfilter
from .Project import *
from .Run_Simulation import *
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import requests
from plotly.offline import plot
from plotly.graph_objs import Scatter

from django.urls import path

#I creata a golobal function that will be call by the view to create the filter of the ECa tables

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 100000


""" Lets try to use Chart.js with django API framework""" 
class ChartData(APIView):
    pagination_class = LargeResultsSetPagination()
    authentication_classes = []
    permission_classes = []


    def get(self, request, format=None):
        #Query set for all acceptance criteria
        qs_ACC = AcceptanceCriteria.objects.all().values()
        ECA_ID = [eca['id'] for eca in qs_ACC]

        #Query set for all welding configurations
        qs_weld_configuration = weld_configuration.objects.all().values()
        WELD_ID = [weld['id'] for weld in qs_weld_configuration]

        #Initialisation of the dictionnary for storing results 
        eca_simulation_resuslts = []
        simulation_result = {}
        eca_result = {}
        data={}
        test={}
        for eca_id in ECA_ID:
            for weld_id in WELD_ID:
                data={}
                sim_weldc = {'weld_configuration' : pd.DataFrame({'WT (mm)' : [30],
                                                                'OD_inch': [30]}),}
                repair_data = { 'repair_data' : pd.DataFrame({'Minumum value of internal ligament for partial repair (mm)' : [6.0], 
                                        'Min excavation length at bottom excavation (mm)' : [50],
                                        'Max excavation length at OD for PR (% pipe circumference)' : [0.3],
                                        'Max excavation length at OD for TTR (% pipe circumference)' : [0.2],})}
                OBJECTS = [PlanarIndicationAcceptanceCriteria, ConcavitySaggingCriteria ,PorosityCriteria, ClusterPorosityCriteria, SlagCriteria, Other1Criteria, Other2Criteria, Other3Criteria, Other4Criteria, Other5Criteria ]
                object_name = [object._meta.object_name for object in OBJECTS]
                d = {name : pd.DataFrame() for name in object_name}
                for object in OBJECTS:
                    query = object.objects.filter(AcceptanceCriteria=eca_id).values()
                    df = pd.DataFrame(query)
                    if object._meta.object_name == 'ConcavitySaggingCriteria':
                        for i in range(2):
                            new_columns = df[df['weld_thickness_zone']==i][['max_height', 'max_length']]
                            new_columns.columns = ['max_height'+str(i), 'max_length' +str(i)]
                            new_columns.reset_index(drop=True, inplace=True)
                            d[object._meta.object_name]['max_height'+str(i)] = new_columns['max_height'+str(i)]
                            d[object._meta.object_name]['max_length'+str(i)] = new_columns['max_length'+str(i)]
                    else:
                        for i in range (10):
                            new_columns = df[df['weld_thickness_zone']==i][['max_height', 'max_length']]
                            new_columns.columns = ['max_height'+str(i), 'max_length' +str(i)]
                            new_columns.reset_index(drop=True, inplace=True)
                            d[object._meta.object_name]['max_height'+str(i)] = new_columns['max_height'+str(i)]
                            d[object._meta.object_name]['max_length'+str(i)] = new_columns['max_length'+str(i)]
                
                indications_query = aut_indications.objects.filter(weld_configuration_id=weld_id).values()
                df_indications = pd.DataFrame(indications_query)
                indications_dict = { 'defect_log' : df_indications}
                d.update(indications_dict)
                d.update(sim_weldc)
                d.update(repair_data)
                Simulation_Project = AUT_Project(d)
                Simulation = Results_Simulation(Simulation_Project).Simulation_Data()

                for columns in Simulation.columns:
                    Simulation_Project.AUT_indication[columns] = Simulation[columns]
                data2 = Simulation_Project.AUT_indication.to_dict(orient='records')
                eca_simulation_resuslts.append({'ecaid' : eca_id,
                                                'weldid' : weld_id,
                                                'data': data2})

        data=eca_simulation_resuslts
        return Response(data)



def filter_ECA(request):
    qs_ACC = AcceptanceCriteria.objects.all().values()
    myFilter = ECAfilter(request.GET, queryset = qs_ACC)
    qs_ACC= myFilter.qs
    return (qs_ACC, myFilter)

def filter_Weldconfiguration(request):
    qs_weldconfig = weld_configuration.objects.all().values()
    myFilter = WeldConfigfilter(request.GET, queryset=qs_weldconfig)
    qs_weldconfig = myFilter.qs
    return(qs_weldconfig, myFilter)
