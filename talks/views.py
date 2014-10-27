from django.http import HttpResponse
from django.views.generic import View


class TalkListDetailView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('a talk list')
