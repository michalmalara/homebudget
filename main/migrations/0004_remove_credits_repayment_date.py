# Generated by Django 3.0.3 on 2020-02-11 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_accounts_is_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credits',
            name='repayment_date',
        ),
    ]
