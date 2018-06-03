from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

from website_core.models import Event, NewsItem, JobOffer, DateItem, NewsletterIssue


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


def ListViewFactory(model):
    """ Factory function for ListViews of *published* model instances

    Templates must be stored in templates/generic/<lowercase model name>_list.html
    """

    if not getattr(model, 'published'):
        raise AttributeError(f'Model {model.__name__} has no "published" attribute')

    class LV(ListView):
        queryset = model.objects.filter(published=True).order_by('-date_created')
        template_name = f'generic/{model.__name__.lower()}_list.html'
        pagination = 50

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['now'] = timezone.now()
            return context
    return LV.as_view()


def index(request):
    """ View for the index page
    Gives access to the following in the template:

    news_items - list of 10 news items ordered by decreasing date of creation
    job_offers - list of 10 job offers ordered by decreasing date of creation
    events - list of the 10 next deadlines for events ordered by decreasing date
    """

    return render(request, 'index.html', {
        'news_items': NewsItem.objects.filter(tags__name__in=['front'], published=True).order_by('-date_created')[:10],
        'job_offers': JobOffer.objects.filter(published=True).order_by('-date_created')[:10],
        'events': DateItem.objects.filter(event__published=True).filter(date__gte=timezone.now()).order_by('-date')[:10]
        # 'events':
        # Event.objects.filter(published=True).order_by('-date__date').distinct()[:10],
    })


def single_newsletter(request, year, month):
    """Returns a single newsletter identified with year and month or 404"""

    newsletter = get_object_or_404(NewsletterIssue, date__month=month, date__year=year)
    return render(request, 'newsletter-detail.html', {'nl': newsletter})
