# Generated by Django 2.0.5 on 2018-09-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_post_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='full_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]