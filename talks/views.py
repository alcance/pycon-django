from __future__ import absolute_import

from django.http import HttpResponse
from django.views.generic import View, ListView

from braces.views import LoginRequiredMixin

from .models import TalkList


class TalkListListView(
    LoginRequiredMixin,
    ListView
):
    model = TalkList

    def get_queryset(self):
        return self.request.user.lists.all()


class TalkListDetailView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('a talk list')
