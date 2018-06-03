from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from datetime import date

from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from website_core.models import JobOffer, Event, DateItem, FileItem, NewsItem


class DateInlineAdmin(admin.TabularInline):
    model = DateItem


class FileInlineAdmin(GenericTabularInline):
    model = FileItem


@admin.register(Event)
class EventAdmin(MarkdownxModelAdmin):

    inlines = [DateInlineAdmin, FileInlineAdmin]


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):

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


admin.site.register(DateItem)
admin.site.register(FileItem)
