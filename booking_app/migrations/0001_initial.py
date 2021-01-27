# Generated by Django 3.1.5 on 2021-01-27 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_num', models.IntegerField()),
            ],
            options={
                'db_table': 'floor',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.IntegerField()),
                ('row', models.CharField(max_length=10)),
                ('seat_num', models.IntegerField()),
            ],
            options={
                'db_table': 'seat',
            },
        ),
        migrations.CreateModel(
            name='SeatBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('shift', models.CharField(max_length=10)),
                ('booked_by', models.CharField(max_length=500)),
                ('floor', models.IntegerField()),
                ('seat_row', models.CharField(max_length=10)),
                ('seat_num', models.IntegerField()),
                ('seat_id', models.IntegerField()),
            ],
            options={
                'db_table': 'seatbooking',
            },
        ),
    ]
