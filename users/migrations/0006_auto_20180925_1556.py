# Generated by Django 2.0.5 on 2018-09-25 12:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_auto_20180925_1010'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfil',
            new_name='UserProfile',
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Kullanıcı Bilgileri', 'verbose_name_plural': 'Kullanıcı Bilgileri'},
        ),
    ]
