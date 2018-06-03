from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.utils import timezone

from website_core.models import Event, NewsItem, JobOffer, DateItem


def DetailViewFactory(model):
    """ Factory function for DetailViews of *published* model instances

    Templates must be stored in templates/generic/<lowercase model name>_detail.html
    """

    if not getattr(model, 'published'):
        raise AttributeError(f'Model {model.__name__} has no "published" attribute')

    class DV(DetailView):
        queryset = model.objects.filter(published=True)
        template_name = f'generic/{model.__name__.lower()}_detail.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['now'] = timezone.now()
            return context
    return DV.as_view()
