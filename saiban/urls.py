from django.conf.urls import patterns, url, include

from controllers import views, api

urlpatterns = patterns('',
    # Landing
    url(r'^$', views.index, name='index'),
    # Auth
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    # Profile
    url(r'^profile/', views.profile, name='profile'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^quiz/', views.quiz, name='quiz'),
    # API
    url(r'^api/random-group/', api.random_group, name='random-group'),
)
