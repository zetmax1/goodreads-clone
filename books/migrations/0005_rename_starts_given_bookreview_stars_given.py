# Generated by Django 5.2.3 on 2025-06-24 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_bookreview_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookreview',
            old_name='starts_given',
            new_name='stars_given',
        ),
    ]
