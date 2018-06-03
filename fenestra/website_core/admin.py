from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from datetime import date

from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from website_core.models import JobOffer, Event, DateItem, FileItem, NewsItem, NewsletterIssue


class DateInlineAdmin(admin.TabularInline):
    model = DateItem


class FileInlineAdmin(GenericTabularInline):
    model = FileItem


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'date', 'location', 'published')
    list_filter = ('published',)
    list_editable = ('published', )

    fieldsets = (
        (None, {
            'fields': (('name', 'short_name'), 'published'),
        }),
        ('Location', {
            'fields': ('location', ('gps_lat', 'gps_lon')),
        }),
        ('About', {
            'fields': ('short_description', 'description'),
        })
    )
    inlines = [DateInlineAdmin, FileInlineAdmin]


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):

    list_display = ('position', 'entity', 'location', 'date_created', 'published')
    list_filter = ('published',)
    list_editable = ('published',)

    fieldsets = (
        (None, {
            'fields': ('position', 'entity', 'published'),
        }),
        ('Location', {
            'fields': ('location', ('gps_lat', 'gps_lon')),
        }),
        ('Description', {
            'fields': ('description',),
        })
    )
    inlines = [FileInlineAdmin]



class NewsItemForm(forms.ModelForm):

    class Meta:
        model = NewsItem
        exclude = ['tags']

    tags = TagField(required=False, widget=LabelWidget)
    tags.help_text = '<em>Important!</em> Tags to apply.<ul><li><em>Frontpage:</em> show on frontpage</li><li><em>YAN:</em> Show on YAN page</li></ul>'


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):

    list_display = ('title', 'date_created', 'date_modified', 'tag_list', 'published')
    list_filter = ('published',)
    list_editable = ('published',)
    form = NewsItemForm

    fieldsets = (
        (None, {
            'fields': ('title', 'tags', 'image', 'published'),
        }),
        ('Content', {
            'fields': ('content',)
        })
    )
    inlines = [FileInlineAdmin]


    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(NewsletterIssue)
class NewsletterIssueAdmin(admin.ModelAdmin):

    list_filter = ('date',)
    fieldsets = (
        (None, {
            'fields': ('date', 'free_text'),
        }),
        ('News', { 'fields': ('news',), }),
        ('Events', { 'fields': ('dates',), }),
        ('Job Offers', { 'fields': ('jobs',), }),
    )

    inlines = [FileInlineAdmin]

    def get_field_queryset(self, db, db_field, request):

        if db_field.name in ['news', 'jobs']:
            return db_field.remote_field.model._default_manager.filter(published=True).order_by('-date_created')
        if db_field.name == 'dates':
            return db_field.remote_field.model._default_manager.filter(event__published=True).order_by('date')
        super().get_field_queryset(db, db_field, request)


admin.site.register(DateItem)
admin.site.register(FileItem)
