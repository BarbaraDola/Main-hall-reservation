# Generated by Django 3.2.11 on 2022-01-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainHall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('room_capacity', models.IntegerField()),
                ('projector', models.BooleanField(default=False)),
            ],
        ),
    ]