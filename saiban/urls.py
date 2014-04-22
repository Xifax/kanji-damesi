from django.conf.urls import patterns, url, include

from saiban import views

# from tastypie.api import Api
# from api import (
#     KanjiResource,
#     KanjiGroupResource,
#     QuizResource
# )
#
# api = Api(api_name='quiz')
# api.register(KanjiResource())
# api.register(KanjiGroupResource())
# api.register(QuizResource())
#
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^quiz/', views.quiz, name='quiz'),
    # url(r'^api/', include(api.urls)),
    url(r'^api/next-group/', views.next_group, name='next-group'),
)
