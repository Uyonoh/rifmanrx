# Generated by Django 5.0.6 on 2024-07-27 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0018_alter_drug_day_added'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Injectible',
            new_name='Injectable',
        ),
    ]
