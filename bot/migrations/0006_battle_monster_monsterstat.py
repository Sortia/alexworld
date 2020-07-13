# Generated by Django 3.0.8 on 2020-07-12 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20200712_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=5000, null=True)),
                ('hp', models.IntegerField()),
                ('min_damage', models.IntegerField()),
                ('max_damage', models.IntegerField()),
                ('attack_speed', models.IntegerField()),
                ('win_speech', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MonsterStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('monster', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Monster')),
                ('stat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Stat')),
            ],
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_win', models.BooleanField(null=True)),
                ('actions', models.CharField(max_length=100000)),
                ('monster', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Monster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bot.User')),
            ],
        ),
    ]
