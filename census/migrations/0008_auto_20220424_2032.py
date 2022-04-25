# Generated by Django 3.2.5 on 2022-04-25 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0007_dataprofilevars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataprofilevars',
            name='variables',
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='attributes',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='concept',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='group',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='hasGeoCollectionSupport',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='label',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='limit',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='predicateOnly',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='predicateType',
            field=models.CharField(default='na', max_length=255),
        ),
        migrations.AddField(
            model_name='dataprofilevars',
            name='required',
            field=models.CharField(default='na', max_length=255),
        ),
    ]
