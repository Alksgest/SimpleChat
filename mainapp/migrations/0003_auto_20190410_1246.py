# Generated by Django 2.1.7 on 2019-04-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_chatroom_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='date',
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='password',
            field=models.CharField(default='616', max_length=24, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='title',
            field=models.CharField(max_length=30, unique=True, verbose_name='Title'),
        ),
    ]