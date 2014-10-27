from django.conf.urls import patterns, include, url

from .views import TalkListDetailView, TalkListListView

list_patterns = patterns(
    '',
    url(r'', TalkListListView.as_view(), name='list'),
    url(
        r'^\d(?P<slug>[-\w]+)/$',
        TalkListDetailView.as_view(),
        name='detail'
    ),
)
urlpatterns = patterns(
    '',
    url(r'^lists/', include(list_patterns, namespace='lists')),
)
