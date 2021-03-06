# Generated by Django 3.2.11 on 2022-01-09 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField(null=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation_app.mainhall')),
            ],
            options={
                'unique_together': {('room_id', 'date')},
            },
        ),
    ]
