# Generated by Django 2.0.5 on 2018-05-28 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='files',
            field=models.ManyToManyField(null=True, to='website_core.FileItem'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='files',
            field=models.ManyToManyField(null=True, to='website_core.FileItem'),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='files',
            field=models.ManyToManyField(null=True, to='website_core.FileItem'),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/news/%Y%m%d/'),
        ),
    ]