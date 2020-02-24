# Generated by Django 3.0.3 on 2020-02-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200213_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('date', models.DateField()),
                ('jedzenie', models.FloatField()),
                ('chemia', models.FloatField()),
                ('kosmetyki', models.FloatField()),
                ('dom', models.FloatField()),
                ('transport', models.FloatField()),
                ('inne', models.FloatField()),
            ],
        ),
    ]
