# Generated by Django 3.0.4 on 2020-04-24 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instalikes', '0002_auto_20200424_1438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likedby',
            old_name='image_id',
            new_name='image',
        ),
    ]
