# Generated by Django 2.0.5 on 2018-10-01 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_auto_20181001_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='etiket',
            field=models.ManyToManyField(null=True, related_name='post', to='posts.Tag', verbose_name='Etiketler'),
        ),
    ]
