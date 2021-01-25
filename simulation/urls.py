from django.urls import path
from .views import  ChartData

app_name = 'simulation'
urlpatterns = [
    path('api/data/', ChartData.as_view()),
]
