# Generated by Django 2.0.5 on 2018-10-01 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0026_remove_post_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='isim',
            field=models.CharField(blank=True, max_length=20, verbose_name='Etiket'),
        ),
    ]
