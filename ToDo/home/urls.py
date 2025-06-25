from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('today/', views.today, name='today'),
    # path('all/', views.all, name='all'),
    # path('flagged/', views.flagged, name='flagged'),
    # path('completed/', views.completed, name='completed'),
    # path('add/', views.add, name='add'),
    # path('flag/', views.flag, name='flag'),
    
    
]