# Generated by Django 2.1.7 on 2019-04-11 06:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20190410_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chatRoom',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mainapp.ChatRoom', verbose_name='ChatRoom'),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 11, 9, 21, 30, 35570), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='user',
            name='chatRooms',
            field=models.ManyToManyField(related_name='users', to='mainapp.ChatRoom'),
        ),
    ]
