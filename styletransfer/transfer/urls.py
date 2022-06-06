from django.urls import path,  include
from .views import *


urlpatterns = [
    path(r'main', index, name='index' ),
    path(r'result/<int:folder>', result, name ='result'),
    path(r'index', index, name ='index'),
    path(r'home', home, name ='home'),
    path(r'readme', readme, name ='readme'),
    path(r'developer', developer, name ='developer')
]




