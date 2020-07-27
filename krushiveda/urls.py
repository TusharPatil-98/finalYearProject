from django.urls import path

from . import views
from .views import FarmerQueriePage

urlpatterns = [
    path('apiTransaction', views.index),
    path('apiTransaction/getDiseaseInfo', views.disease_info),
    path('apiTransaction/helpline', views.helpline),
    path('apiTransaction/startupQuery', views.StartUpQuery),
    path('apiTransaction/check', views.check_pending_queries),
    path('query_operator', views.query_operator),
    path('farmer_query', FarmerQueriePage.as_view()),
    path('runModel', views.train),

]