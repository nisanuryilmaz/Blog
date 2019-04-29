# Generated by Django 2.0.5 on 2018-08-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20180811_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False, verbose_name='Taslak oluşturulsun mu?'),
        ),
        migrations.AlterField(
            model_name='category',
            name='kategori_adi',
            field=models.CharField(max_length=120, verbose_name='Kategori adı'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='İçerik'),
        ),
        migrations.AlterField(
            model_name='post',
            name='kategori',
            field=models.ManyToManyField(related_name='post', to='posts.Category', verbose_name='Kategoriler'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=120, verbose_name='Başlık'),
        ),
    ]
