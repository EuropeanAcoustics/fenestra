from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.utils import timezone

from website_core.models import Event


class EventDetailView(DetailView):
    model = Event
    template_name = 'generic/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
