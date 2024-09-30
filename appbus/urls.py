from django.urls import path
from .views import IndexView,BaseView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('base/',BaseView.as_view(), name='base'),
]