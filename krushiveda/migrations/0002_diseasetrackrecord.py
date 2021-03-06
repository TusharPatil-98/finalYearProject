# Generated by Django 2.2.7 on 2020-07-01 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('krushiveda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseTrackRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.BigIntegerField()),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('disease', models.CharField(max_length=200)),
                ('notified', models.BooleanField(default=False)),
                ('dateTime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
