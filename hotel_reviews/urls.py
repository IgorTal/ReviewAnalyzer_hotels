from django.conf.urls import url 
from . import views 

#add a url /home for this app 

urlpatterns = [ 
    url(r'^$', views.home, name='home'), 
    ]
