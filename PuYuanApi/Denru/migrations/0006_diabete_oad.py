# Generated by Django 3.1.1 on 2020-10-20 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Denru', '0005_remove_diabete_oad'),
    ]

    operations = [
        migrations.AddField(
            model_name='diabete',
            name='oad',
            field=models.CharField(max_length=20, null=True),
        ),
    ]