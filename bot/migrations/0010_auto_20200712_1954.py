# Generated by Django 3.0.8 on 2020-07-12 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_auto_20200712_1937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='battle',
            old_name='actions',
            new_name='data',
        ),
    ]
