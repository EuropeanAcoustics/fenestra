from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from taggit.managers import TaggableManager
from taggit_labels.widgets import LabelWidget
from autoslug import AutoSlugField
from markdownx.models import MarkdownxField


DATE_ITEM_CHOICES = (
    ('abs_end', 'Abstract Submission Deadline'),
    ('art_end', 'Article Submission Deadline'),
    ('abs_beg', 'Abstract Submission starts'),
    ('accept', 'Acceptation notice'),
    ('reg_end', 'Registration Deadline'),
    ('erg_end', 'Early Registration Deadline'),
    ('other', 'Other')
)


class FileItem(models.Model):
    """ Holds a file attachment
    description -
    item - File object"""

    description = models.CharField(max_length=100)
    item = models.FileField(upload_to='uploads/files/%Y%m%d/')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.description


class NewsItem(models.Model):
    """ News item
    title -
    content - text to be displayed in the news
    published - boolean for the news item to appear online

    date_created - (auto) date of first insertion in database
    date_modified - (auto) updated every time the item is saved

    image - image for the title

    files - attachements
    """

    title = models.CharField(max_length=160)
    content = models.TextField()
    tags = TaggableManager()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    image = models.ImageField(null=True, blank=True, upload_to='uploads/news/%Y%m%d/')

    files = GenericRelation(FileItem)

    def __str__(self):
        return f'News on {self.date_modified}: {self.title}'


class JobOffer(models.Model):
    """Job offer item
    position -
    entity - entity offering the position
    location - (blank) where the job is offered
    published - boolean for the job to be listed on the website

    date_created - (auto) date of inserting in the DB

    gps_lat - GPS coordinates (for mapping purposes)
    gps_lon - GPS coordinates (for mapping purposes)
    files - List of attached FileItem
    """

    position = models.CharField(max_length=160)
    entity = models.CharField(max_length=100)
    entity.help_text = 'Institution (univ., agency or company) that offers the job'
    location = models.CharField(max_length=100)
    published = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)

    gps_lat = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    gps_lon = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    files = GenericRelation(FileItem)

    def __str__(self):
        return f'{self.position} at {self.entity} in {self.location}'


class Event(models.Model):
    """ Event item (conference, workshop, etc.)
    name -
    short_name - (blank) Acronym or short version
    short_description - Description of the event in 160 char
    description -
    slug - (auto) URL Friendly slug
    published - is the item seen on lists and feeds ?

    location - (blank) where the event happens
    gps_lat - GPS coordinates (for mapping purposes)
    gps_lon - GPS coordinates (for mapping purposes)
    files - List of attached FileItem
    """

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=15, null=True, blank=True)
    short_description = models.CharField(max_length=100, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    published = models.BooleanField(default=True)
    description = MarkdownxField()

    location = models.CharField(max_length=100)
    gps_lat = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    gps_lon = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    files = GenericRelation(FileItem)

    def __str__(self):
        return self.name


class DateItem(models.Model):
    """ Stores a Date (deadline, regsitration, etc.)
    event - FK to related event
    date -
    typ - Type of date, see choices at beginning of file
    description - To be used is typ=Other
    extended - boolean to mark extended deadlinnes
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()

    typ = models.CharField(max_length=7, name='type', choices=DATE_ITEM_CHOICES)
    description = models.CharField(max_length=100, null=True, blank=True)
    description.help_text = 'Only if type is "Other"'
    extended = models.BooleanField(default=False)

    def __str__(self):
        pfx = 'Extended ' if self.extended else ''
        sfx = f': {self.description}'
        return f'{self.date} {pfx}{self.type}{sfx}'
