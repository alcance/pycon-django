from django.conf.urls import patterns, include, url

from .views import (
    TalkListDetailView,
    TalkListListView,
    TalkListCreateView
)

list_patterns = patterns(
    '',
    url(r'^$', TalkListListView.as_view(), name='list'),
    url(r'^create/$', TalkListCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/$', TalkListDetailView.as_view(), name='detail'),
)
urlpatterns = patterns(
    '',
    url(r'^lists/', include(list_patterns, namespace='lists')),
)
