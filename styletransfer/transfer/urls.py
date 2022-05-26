from django.urls import path,  include
from .views import *


urlpatterns = [
    path('', index, name='index' ),
    path('result', result, name ='result'),
    path('index', index, name ='index'),
    path('mainpage', mainpage, name ='mainpage'),
    path('readme', readme, name ='readme'),
    path('developer', developer, name ='developer')
]




