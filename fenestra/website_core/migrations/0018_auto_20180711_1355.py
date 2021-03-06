# Generated by Django 2.0.5 on 2018-07-11 13:55

import autoslug.fields
from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('website_core', '0017_auto_20180711_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.CharField(blank=True, max_length=120, null=True)),
                ('published', models.BooleanField(default=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(max_length=70, unique=True)),
                ('extra_head', models.TextField(blank=True, null=True)),
                ('content', markdownx.models.MarkdownxField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='organisation',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, populate_from='name', unique=True),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='page',
            index=models.Index(fields=['url'], name='website_cor_url_98d20a_idx'),
        ),
    ]
