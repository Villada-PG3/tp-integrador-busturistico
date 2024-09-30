from django.shortcuts import render,redirect
from django.views.generic import TemplateView
import requests
from typing import Any

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
class BaseView(TemplateView):
    template_name = 'base/base.html'