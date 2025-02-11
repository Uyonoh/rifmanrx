# Generated by Django 5.0.6 on 2024-07-30 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_purchase_drug_alter_sale_drug'),
        ('drugs', '0021_alter_drug_day_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='drug',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drugs.drug'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='drug',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drugs.drug'),
        ),
    ]
