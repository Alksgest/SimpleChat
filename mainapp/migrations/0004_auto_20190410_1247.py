# Generated by Django 2.1.7 on 2019-04-10 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20190410_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chatRoom',
        ),
        migrations.RemoveField(
            model_name='message',
            name='owner',
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='password',
            field=models.CharField(default='486', max_length=24, verbose_name='Password'),
        ),
    ]