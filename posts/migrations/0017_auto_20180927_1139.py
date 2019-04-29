# Generated by Django 2.0.5 on 2018-09-27 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_post_etiket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etiket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiket', models.CharField(max_length=20, verbose_name='Etiket')),
            ],
            options={
                'verbose_name': 'Etiket',
                'verbose_name_plural': 'Etiketler',
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='etiket',
        ),
        migrations.AddField(
            model_name='etiket',
            name='gonderi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etiket', to='posts.Post', verbose_name='Post'),
        ),
    ]
