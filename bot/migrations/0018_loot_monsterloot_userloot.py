# Generated by Django 3.0.8 on 2020-07-14 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0017_auto_20200714_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserLoot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('loot', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bot.Loot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='loot', to='bot.User')),
            ],
        ),
        migrations.CreateModel(
            name='MonsterLoot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_count', models.IntegerField()),
                ('max_count', models.IntegerField()),
                ('loot', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='monsters', to='bot.Loot')),
                ('monster', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='loot', to='bot.Monster')),
            ],
        ),
    ]