# Generated by Django 2.0.5 on 2018-09-29 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_post_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='full_name',
        ),
    ]
