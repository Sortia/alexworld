# Generated by Django 3.0.8 on 2020-07-13 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0013_auto_20200713_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='battle', to='bot.User'),
        ),
        migrations.AlterField(
            model_name='specializationstat',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stats', to='bot.Specialization'),
        ),
    ]
