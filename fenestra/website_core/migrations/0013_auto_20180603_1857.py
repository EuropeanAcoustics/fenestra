# Generated by Django 2.0.5 on 2018-06-03 18:57

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('website_core', '0012_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dateitem',
            name='type',
            field=models.CharField(choices=[('abs_end', 'Abstract Submission Deadline'), ('art_end', 'Article Submission Deadline'), ('abs_beg', 'Abstract Submission starts'), ('accept', 'Acceptation notice'), ('reg_end', 'Registration Deadline'), ('erg_end', 'Early Registration Deadline'), ('occurs', 'Event occurs'), ('other', 'Other')], max_length=7),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]
