# Generated by Django 3.1.1 on 2020-10-26 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('invite_code', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Friend_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('relation_id', models.CharField(blank=True, max_length=100)),
                ('friend_type', models.IntegerField(blank=True)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('read', models.BooleanField(blank=True, default=False)),
                ('imread', models.BooleanField(blank=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
