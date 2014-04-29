from django.conf.urls import patterns, url, include

from controllers import views, api

urlpatterns = patterns('',
    # Landing
    url(r'^$', views.index, name='index'),
    # Auth
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^try/', views.try_quiz, name='try'),
    # Profile
    url(r'^profile/', views.profile, name='profile'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^quiz/', views.quiz, name='quiz'),
    # API
    url(r'^api/random-group/', api.random_group, name='random-group'),
    url(r'^api/next-group/', api.next_group, name='next-group'),
    url(r'^api/answer/', api.process_answer, name='answer'),
    url(r'^api/skip/', api.skip_kanji, name='skip-kanji'),
)
