# Generated by Django 2.1.3 on 2018-11-25 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppl_registration', '0004_auto_20181125_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='spots_available',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='waitlist_spots_available',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
