# Generated by Django 3.0.4 on 2020-05-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instalikes', '0013_post_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='figcaption',
            field=models.CharField(default='', max_length=225),
        ),
    ]
