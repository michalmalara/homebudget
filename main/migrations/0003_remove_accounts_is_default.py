# Generated by Django 3.0.3 on 2020-02-11 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_credits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='is_default',
        ),
    ]
