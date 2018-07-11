"""fenestra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include

from website_core.views import DetailViewFactory, ListViewFactory
import website_core.views as wc_views
from website_core.models import Event, NewsItem, JobOffer


urlpatterns = [
    path('', wc_views.index, name='index'),
    path('events/<slug:slug>/', DetailViewFactory(Event), name='event-detail'),
    path('news/<slug:slug>/', DetailViewFactory(NewsItem), name='newsitem-detail'),
    path('jobs/<slug:slug>/', DetailViewFactory(JobOffer), name='joboffer-detail'),
    path('organisations/<slug:slug>/', wc_views.OrganisationsDetail.as_view(), name='organisation-detail'),
    path('news/', ListViewFactory(NewsItem), name='newsitem-list'),
    path('jobs/', ListViewFactory(JobOffer), name='joboffer-list'),
    path('organisations/', wc_views.OrganisationsList.as_view(), name='organisation-list'),
    path('nuntius/<int:year>/<int:month>/', wc_views.single_newsletter, name='newsletter-detail'),
    re_path(r'^p/(?P<url>[a-z/]+)$', wc_views.page, name='page'),
]
