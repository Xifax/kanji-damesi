from django.conf.urls import patterns, url

from controllers import views, api

urlpatterns = patterns(
    '',
    # Landing
    url(r'^$', views.index, name='index'),
    # Auth
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^switch/', views.switch, name='switch'),
    url(r'^register/', views.register, name='register'),
    url(r'^try/', views.try_quiz, name='try'),
    # Profile
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/achievements/', views.achievements, name='achievements'),
    url(r'^profile/history/', views.history, name='history'),
    url(r'^profile/stats/', views.stats, name='stats'),
    url(r'^quiz/', views.quiz, name='quiz'),
    # Quiz API
    url(r'^api/random-group/', api.random_group, name='random-group'),
    url(r'^api/next-group/', api.next_group, name='next-group'),
    url(r'^api/answer/', api.process_answer, name='answer'),
    url(r'^api/skip/', api.skip_kanji, name='skip-kanji'),
    # Profile API
    url(r'^api/get-level/', api.get_level, name='get-level'),
    url(r'^api/change-level/', api.change_level, name='change-level'),
    url(r'^api/get-kanji/(?P<id>\d+)/$',
        api.get_kanji, name='get-kanji'),
)
