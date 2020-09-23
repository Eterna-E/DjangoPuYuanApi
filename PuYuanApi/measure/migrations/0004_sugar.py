# Generated by Django 3.1.1 on 2020-09-23 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measure', '0003_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sugar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sugar', models.DecimalField(decimal_places=0, max_digits=10)),
                ('timeperiod', models.DecimalField(decimal_places=0, max_digits=10)),
                ('recorded_at', models.DateTimeField()),
            ],
        ),
    ]
