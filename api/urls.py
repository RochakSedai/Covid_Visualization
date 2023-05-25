from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tabular_form', views.get_table, name='get_table'),
    path('visualize_world', views.visualize_world, name='visualize_world'),
    path('visualize_nepal', views.visualize_nepal, name='visualize_nepal'),
    path('visualize_world/heatmap', views.world_heatmap, name='heatmap' )
]