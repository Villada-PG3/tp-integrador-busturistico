from django.urls import path
from .views import IndexView,BaseView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('base/',BaseView.as_view(), name='base'),
    path('recorrido/',RecorridoView.as_view(), name='recorrido'),
    path('parada/<int:id>/',ParadaView.as_view(), name='parada'),
]
