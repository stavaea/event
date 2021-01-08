from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'register/$', views.register),
    url(r'submit_info/$', views.result),
    url(r'user_login/$', views.user_login),
    url(r'login/$', views.login),
    url(r'search_user/$', views.search_user),
    url(r'show/$', views.show),
    url(r'^searchbyname/$', views.searchbyname),
]