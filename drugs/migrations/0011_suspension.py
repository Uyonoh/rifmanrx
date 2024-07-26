# Generated by Django 5.0.6 on 2024-07-25 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0010_alter_drug_day_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suspension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_bottles', models.IntegerField()),
                ('no_packs', models.IntegerField(default=1, null=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspension',
            name='no_bottles',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='suspension',
            name='no_packs',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='suspension',
            name='drug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug'),
        ),
    ]
