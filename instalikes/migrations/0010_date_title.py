# Generated by Django 3.0.4 on 2020-05-22 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instalikes', '0009_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='date',
            name='title',
            field=models.CharField(default=' ', max_length=225),
        ),
    ]
