# Generated by Django 3.2.3 on 2021-06-25 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beholder', '0002_issue_cover_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bio',
            name='bio_img_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='bio',
            name='person_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='bio',
            name='social_url',
            field=models.URLField(blank=True),
        ),
    ]
