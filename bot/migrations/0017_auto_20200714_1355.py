# Generated by Django 3.0.8 on 2020-07-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0016_auto_20200714_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='energy',
            field=models.IntegerField(default=1000),
        ),
    ]