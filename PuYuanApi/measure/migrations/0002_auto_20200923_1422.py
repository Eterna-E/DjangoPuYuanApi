# Generated by Django 3.1.1 on 2020-09-23 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measure', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pressure',
            name='recorded_at',
            field=models.DateTimeField(),
        ),
    ]
