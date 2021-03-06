# Generated by Django 2.0.5 on 2018-09-22 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0012_auto_20180917_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='isim_soyisim',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users_comment', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='icerik',
            field=models.TextField(max_length=1000, verbose_name='Yorum'),
        ),
    ]
