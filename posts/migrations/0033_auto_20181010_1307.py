# Generated by Django 2.0.5 on 2018-10-10 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0032_commentchild'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Comment', verbose_name='comment_like')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Beğenilen Yorumlar',
                'verbose_name_plural': 'Beğenilen Yorumlar',
            },
        ),
        migrations.AlterModelOptions(
            name='commentchild',
            options={'ordering': ['tarih'], 'verbose_name': 'İç İçe Yorum', 'verbose_name_plural': 'İçe İçe Yorumlar'},
        ),
    ]
