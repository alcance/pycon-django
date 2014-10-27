from django.conf.urls import patterns, include, url

from .views import TalkListDetailView

list_patterns = patterns(
    '',
    url(r'', TalkListDetailView.as_view(), name='detail'),
)
urlpatterns = patterns(
    '',
    url(r'^lists/$', include(list_patterns, namespace='lists')),
)
