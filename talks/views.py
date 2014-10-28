from __future__ import absolute_import

from django.views.generic import ListView, DetailView

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from .models import TalkList


class TalkListListView(
    LoginRequiredMixin,
    ListView
):
    model = TalkList

    def get_queryset(self):
        return self.request.user.lists.all()


class TalkListDetailView(
    LoginRequiredMixin,
    #PrefetchRelatedMixin,
    DetailView,
):
    model = TalkList
    prefetch_related = ('talks',)
    '''
    prefetch and select related
    select related sql query go get user related to
    tlaklists that are in queryset. is a sql with joins
    you dont go back to the db

    prefetch join two queries.
    '''
    def get_queryset(self):
        queryset = super(TalkListDetailView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
