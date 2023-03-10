from django.urls import path
from . import views

# URL Config -> Every app can have their own url config, but need to put it 
#   in the main url config
urlpatterns = [
    path('results/', views.get_results),
    path('', views.get_index)
]