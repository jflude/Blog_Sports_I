# Generated by Django 2.2 on 2020-02-24 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleMLB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('away_pitcher', models.CharField(max_length=25)),
                ('away_rot', models.IntegerField()),
                ('away_team', models.CharField(max_length=25)),
                ('details', models.CharField(max_length=25)),
                ('home_pitcher', models.CharField(max_length=25)),
                ('home_rot', models.IntegerField()),
                ('home_team', models.CharField(max_length=25)),
                ('api_id_key', models.CharField(max_length=255)),
                ('match_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='OddsMLB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_id', models.CharField(max_length=255)),
                ('last_updated', models.DateTimeField()),
                ('money_line_away', models.IntegerField()),
                ('money_line_home', models.IntegerField()),
                ('odd_type', models.CharField(max_length=25)),
                ('over_line', models.IntegerField()),
                ('point_spread_away', models.DecimalField(decimal_places=3, max_digits=7)),
                ('point_spread_away_line', models.IntegerField()),
                ('point_spread_home', models.DecimalField(decimal_places=3, max_digits=7)),
                ('point_spread_home_line', models.IntegerField()),
                ('total_number', models.DecimalField(decimal_places=3, max_digits=7)),
                ('under_line', models.IntegerField()),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='odds', to='baseball.ScheduleMLB')),
            ],
        ),
    ]