# Generated by Django 3.0.6 on 2020-05-06 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='author',
            field=models.CharField(default='none', max_length=50, verbose_name='none'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scan',
            name='finish_date',
            field=models.DateTimeField(verbose_name='none'),
        ),
        migrations.AlterField(
            model_name='scan',
            name='start_date',
            field=models.DateTimeField(verbose_name='none'),
        ),
    ]