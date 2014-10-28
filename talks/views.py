from __future__ import absolute_import

from django.contrib import messages
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    RedirectView
)

from braces.views import (
    LoginRequiredMixin,
    PrefetchRelatedMixin,
    SetHeadlineMixin
)

from .models import TalkList, Talk

from .forms import TalkListForm, TalkForm


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

    def get_queryset(self):
        queryset = super(TalkListListView, self).get_queryset()
        queryset = queryset.annotate(talk_count=Count('talks'))
        return queryset


class TalkListDetailView(
    LoginRequiredMixin,
    RestrictToUserMixin,
    PrefetchRelatedMixin,
    DetailView,
):
    form_class = TalkForm
    http_method_names = ['get', 'post']
    model = TalkList
    prefetch_related = ('talks',)

    def get_context_data(self, **kwargs):
        context = super(TalkListDetailView, self).get_context_data(**kwargs)
        context.update({
            'form': self.form_class(self.request.POST or None)
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = self.get_object()
            talk = form.save(commit=False)
            talk.talk_list = obj
            talk.save()
        else:
            return self.get(request, *args, **kwargs)
        return redirect(obj)


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


class TalkListRemoveTalkView(
    LoginRequiredMixin,
    RedirectView
):
    model = Talk

    def get_redirect_url(self, *args, **kwargs):
        return self.talklist.get_absolute_url()

    def get_object(self, pk, talklist_pk):
        try:
            talk = self.model.objects.get(
                pk=pk,
                talk_list_id=talklist_pk,
                talk_list__user=self.request.user
            )
        except Talk.DoesNotExist:
            raise Http404
        else:
            return talk

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            kwargs.get('pk'),
            kwargs.get('talklist_pk')
        )
        self.talklist = self.object.talk_list
        messages.success(
            request,
            u'{0.name} was removed from {1.name}'.format(
                self.object, self.talklist)
        )
        self.object.delete()
        return super(TalkListRemoveTalkView, self).get(request, *args, **kwargs)
