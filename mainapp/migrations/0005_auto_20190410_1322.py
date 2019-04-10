# Generated by Django 2.1.7 on 2019-04-10 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20190410_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='password',
            field=models.CharField(default='sfxf432', max_length=24, verbose_name='Password'),
        ),
    ]
