# Generated by Django 2.0.5 on 2018-09-25 07:04

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180925_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofil',
            name='profilPhoto',
            field=models.ImageField(default='profilPhoto/userprofile.png', upload_to=users.models.upload_to, verbose_name='Profil Fotoğrafı'),
        ),
    ]
