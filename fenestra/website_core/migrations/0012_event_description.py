# Generated by Django 2.0.5 on 2018-06-03 18:36

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('website_core', '0011_auto_20180603_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=markdownx.models.MarkdownxField(default=''),
            preserve_default=False,
        ),
    ]
