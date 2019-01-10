# Generated by Django 2.0.5 on 2018-07-11 12:44

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('website_core', '0016_auto_20180603_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website_url', models.URLField()),
                ('contact_mail', models.EmailField(max_length=254)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='uploads/organisations/')),
                ('free_text', markdownx.models.MarkdownxField(blank=True, null=True)),
                ('map_object', models.TextField()),
                ('on_map', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='position', unique=True),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(blank=True, help_text='Pick one of the existing organisations or use the description field to specify', null=True, on_delete=django.db.models.deletion.SET_NULL, to='website_core.Organisation'),
        ),
    ]