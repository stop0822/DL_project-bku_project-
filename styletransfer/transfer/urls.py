from django.urls import path,  include
from .views import *


urlpatterns = [
    path(r'', index, name='index' ),
    path(r'result/<int:folder>', result, name ='result')
]






