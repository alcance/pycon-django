from __future__ import absolute_import

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)

from braces.views import (
    LoginRequiredMixin,
    PrefetchRelatedMixin,
    SetHeadlineMixin
)

from .models import TalkList

from .forms import TalkListForm


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
    PrefetchRelatedMixin,
    DetailView,
):
    model = TalkList
    prefetch_related = ('talks',)


class TalkListCreateView(
    LoginRequiredMixin,
    SetHeadlineMixin,
    CreateView
):
    form_class = TalkListForm
    headline = 'Create'
    model = TalkList

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TalkListCreateView, self).form_valid(form)


class TalkListUpdateView(
    RestrictToUserMixin,
    LoginRequiredMixin,
    SetHeadlineMixin,
    UpdateView
):
    form_class = TalkListForm
    headline = 'Update'
    model = TalkList
