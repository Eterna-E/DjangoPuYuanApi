# Generated by Django 3.1.1 on 2020-10-20 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Denru', '0004_diabete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diabete',
            name='oad',
        ),
    ]