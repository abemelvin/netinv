# Generated by Django 3.0.6 on 2020-05-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scans', '0005_auto_20200507_0110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='ip_address',
            new_name='ip',
        ),
        migrations.RemoveField(
            model_name='scan',
            name='is_done',
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='device',
            name='first_seen',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='host',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='device',
            name='last_seen',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='scan',
            name='status',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='scan',
            name='author',
            field=models.CharField(max_length=255),
        ),
    ]