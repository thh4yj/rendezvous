# Generated by Django 3.1.1 on 2020-11-06 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('desc', models.TextField(max_length=5000)),
                ('location_name', models.CharField(max_length=50)),
                ('pub_date', models.DateTimeField(verbose_name='Date Published')),
                ('start', models.DateTimeField(verbose_name='Start date')),
                ('end', models.DateTimeField(verbose_name='End date')),
                ('img', models.ImageField(upload_to='images')),
                ('testdg', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
