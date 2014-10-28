from __future__ import absolute_import

from django.views.generic import ListView, DetailView

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from .models import TalkList


class RestrictToUserMixin(object):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class TalkListListView(
    LoginRequiredMixin,
    RestrictToUserMixin,
    ListView
):
    model = TalkList


class TalkListDetailView(
    LoginRequiredMixin,
    RestrictToUserMixin,
    #PrefetchRelatedMixin,
    DetailView,
):
    model = TalkList
    prefetch_related = ('talks',)
