# Generated by Django 2.0.5 on 2019-01-10 12:28

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('website_core', '0019_auto_20180711_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('published', models.BooleanField(default=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('zone', models.IntegerField(choices=[(1, 'Zone 1'), (2, 'Zone 2')])),
                ('focus', models.BooleanField(default=False)),
                ('content', markdownx.models.MarkdownxField(blank=True, null=True)),
            ],
        ),
    ]