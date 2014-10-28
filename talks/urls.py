from django.conf.urls import patterns, include, url

from .views import (
    TalkListDetailView,
    TalkListListView,
    TalkListCreateView,
    TalkListUpdateView,
    TalkListRemoveTalkView,
    TalkListScheduleView
)

list_patterns = patterns(
    '',
    url(r'^$', TalkListListView.as_view(), name='list'),
    url(r'^create/$', TalkListCreateView.as_view(), name='create'),
    url(r'^d/(?P<slug>[-\w]+)/$', TalkListDetailView.as_view(), name='detail'),
    url(r'^e/(?P<slug>[-\w]+)/$', TalkListUpdateView.as_view(), name='update'),
    url(
        r'^remove/(?P<talklist_pk>\d+)/(?P<pk>\d+)/$',
        TalkListRemoveTalkView.as_view(),
        name='remove_talk'
    ),
    url(
        r'^s/(?P<slug>[-\w]+)/$',
        TalkListScheduleView.as_view(),
        name='schedule'
    ),
)
urlpatterns = patterns(
    '',
    url(r'^lists/', include(list_patterns, namespace='lists')),
)
