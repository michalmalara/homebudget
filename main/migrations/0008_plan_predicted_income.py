# Generated by Django 3.0.3 on 2020-02-21 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='predicted_income',
            field=models.FloatField(default=7000.0),
            preserve_default=False,
        ),
    ]
