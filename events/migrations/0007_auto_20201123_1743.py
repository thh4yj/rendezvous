# Generated by Django 3.1.1 on 2020-11-23 22:43

from django.db import migrations, models
import events.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20201113_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='icon',
            field=models.ImageField(blank=True, upload_to='images', validators=[events.validators.validate_file_extension]),
        ),
    ]
