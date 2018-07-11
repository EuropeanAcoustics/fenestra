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
    ('occurs', 'Event occurs'),
    ('other', 'Other')
)
DATE_TYPES = dict(DATE_ITEM_CHOICES)


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
    slug - (auto)
    published - boolean for the news item to appear online

    date_created - (auto) date of first insertion in database
    date_modified - (auto) updated every time the item is saved

    image - image for the title

    files - attachements
    """

    title = models.CharField(max_length=160)
    content = MarkdownxField()
    slug = AutoSlugField(populate_from='title', unique=True)
    tags = TaggableManager()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    image = models.ImageField(null=True, blank=True, upload_to='uploads/news/%Y%m%d/')

    files = GenericRelation(FileItem)

    title.help_text = 'Keep it short and punchy!'
    published.help_text = 'Should the event be displayed publicly?'
    image.help_text = 'Image to be use as title image'

    def __str__(self):
        return f'{self.title} ({self.date_modified.strftime("%Y/%m/%d")})'


class Organisation(models.Model):
    """ Organisation
    Represents a member of the EAA

    name --
    slug -- (auto) based on name
    website_url --
    contact_mail --

    free_text -- to be displayed on the page

    map_object -- JS to be interpreted upon creating the map
    on_map -- boolean controlling display on map
    """

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    website_url = models.URLField()
    contact_mail = models.EmailField()
    logo = models.ImageField(null=True, blank=True, upload_to='uploads/organisations/')

    free_text = MarkdownxField(blank=True, null=True)

    map_object = models.TextField(blank=True, null=True)
    on_map = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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
    description = MarkdownxField(blank=True, null=True)
    slug = AutoSlugField(populate_from='position', unique=True)
    entity = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    published = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)

    gps_lat = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    gps_lon = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    files = GenericRelation(FileItem)

    entity.help_text = 'Institution (univ., agency or company) that offers the job'
    published.help_text = 'Should the event be displayed publicly?'
    gps_lat.help_text = 'GPS Latitute (for mapping purposes)'
    gps_lon.help_text = 'GPS Longitude (for mapping purposes)'

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
    description = MarkdownxField(blank=True, null=True)
    organizer  = models.ForeignKey(Organisation, null=True, blank=True, on_delete=models.SET_NULL)

    location = models.CharField(max_length=100)
    gps_lat = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    gps_lon = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    files = GenericRelation(FileItem)

    published.help_text = 'Should the event be displayed publicly?'
    location.help_text = 'Where does the event happens'
    gps_lat.help_text = 'GPS Latitute (for mapping purposes)'
    gps_lon.help_text = 'GPS Longitude (for mapping purposes)'
    organizer.help_text = 'Pick one of the existing organisations or use the description field to specify'

    def earliest_date(self):
        return self.dates.all().order_by('-date')[0]

    def date(self):
        date_occurs = self.dates.filter(type='occurs')
        if date_occurs:
            return date_occurs[0].date
        else:
            return self.earliest_date().date

    def __str__(self):
        if self.short_name:
            return self.short_name
        else:
            self.name


class DateItem(models.Model):
    """ Stores a Date (deadline, regsitration, etc.)
    event - FK to related event
    date -
    typ - Type of date, see choices at beginning of file
    description - To be used is typ=Other
    extended - boolean to mark extended deadlinnes
    """

    event = models.ForeignKey(Event, related_name='dates', on_delete=models.CASCADE)
    date = models.DateField()

    typ = models.CharField(max_length=7, name='type', choices=DATE_ITEM_CHOICES)
    description = models.CharField(max_length=100, null=True, blank=True)
    description.help_text = 'Only if type is "Other"'
    extended = models.BooleanField(default=False)

    def __str__(self):
        pfx = 'Extended ' if self.extended else ''
        sfx = f': {self.description}' if self.description else ''
        return f'{self.date} {pfx}{DATE_TYPES[self.type]}{sfx}: {self.event}'


class NewsletterIssue(models.Model):
    """ Stores a newsletter issue
    date -
    free_text - text field
    news - news to include
    events - events to include
    jobs - job offers to include
    files - attachments
    """

    date = models.DateField()
    free_text = MarkdownxField(blank=True, null=True)
    news = models.ManyToManyField('NewsItem')
    dates = models.ManyToManyField('DateItem')
    jobs = models.ManyToManyField('JobOffer')
    files = GenericRelation(FileItem)

    def __str__(self):
        return f"Newsletter {self.date.strftime('%Y/%m')}"
