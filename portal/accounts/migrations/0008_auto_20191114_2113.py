# Generated by Django 2.2.6 on 2019-11-14 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20191113_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_administrator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_moderator',
            field=models.BooleanField(default=False),
        ),
    ]
