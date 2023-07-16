from django.urls import path
from .views import GraphView, HeliView

urlpatterns = [
    path('graph/', GraphView.as_view(), name='minimal_way_view'),
    path('heli/', HeliView.as_view(), name='heli_view')
]

