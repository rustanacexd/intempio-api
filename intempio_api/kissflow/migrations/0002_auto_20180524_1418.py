# Generated by Django 2.0.3 on 2018-05-24 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kissflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.CharField(blank=True, default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='exp_participants',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='exp_presenters',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='invite_coming',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='link_needed',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='on_site',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='prod_hours',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='prod_one_confirm',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='prod_start',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='prod_two_confirm',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='producers_req',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='production_ready',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='record_reqs',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='site_address',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
    ]
