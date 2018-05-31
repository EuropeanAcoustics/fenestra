from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from markdownx.admin import MarkdownxModelAdmin

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


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):

    inlines = [FileInlineAdmin]


admin.site.register(DateItem)
admin.site.register(FileItem)
