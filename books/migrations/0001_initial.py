# Generated by Django 5.0.6 on 2024-07-26 19:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drugs', '0017_delete_sale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('price', models.FloatField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
    ]
