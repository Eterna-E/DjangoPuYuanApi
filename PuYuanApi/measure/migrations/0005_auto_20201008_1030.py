# Generated by Django 3.1.1 on 2020-10-08 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measure', '0004_sugar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary_diet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('meal', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('tag', models.CharField(blank=True, max_length=100)),
                ('image_count', models.IntegerField(blank=True)),
                ('lat', models.FloatField(blank=True, max_length=100)),
                ('lng', models.FloatField(blank=True, max_length=100)),
                ('recorded_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='pressure',
            name='diastolic',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='pressure',
            name='pulse',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='pressure',
            name='recorded_at',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='pressure',
            name='systolic',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sugar',
            name='recorded_at',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='sugar',
            name='sugar',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sugar',
            name='timeperiod',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='weight',
            name='bmi',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='weight',
            name='body_fat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='weight',
            name='recorded_at',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='weight',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]
