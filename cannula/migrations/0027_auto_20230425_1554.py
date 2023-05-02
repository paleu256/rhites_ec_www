# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cannula', '0026_ifasbottleneck'),
    ]

    operations = [
        migrations.CreateModel(
            name='district',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='gbvTool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('reporting_period', models.DateField(verbose_name='Reporting Period', auto_now_add=True)),
                ('fd1_2', models.CharField(verbose_name='1.2 Facility offers GBV care without requiring GBV patients to report to the police', max_length=4, default=None, choices=[('None', 'None'), ('No', 'No'), ('Yes', 'Yes')])),
                ('fd1_4', models.CharField(verbose_name='1.4 Facility maintains patient privacy during triage/intake process', max_length=4, default=None, choices=[('None', 'None'), ('No', 'No'), ('Yes', 'Yes')])),
                ('doid', models.ForeignKey(to='cannula.district')),
            ],
        ),
        migrations.CreateModel(
            name='health_facility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('doid', models.ForeignKey(to='cannula.district')),
            ],
        ),
        migrations.CreateModel(
            name='health_subcounty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
                ('hfoid', models.ForeignKey(to='cannula.health_facility')),
            ],
        ),
        migrations.CreateModel(
            name='region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='gbvtool',
            name='hfoid',
            field=models.ForeignKey(to='cannula.health_facility'),
        ),
        migrations.AddField(
            model_name='gbvtool',
            name='roid',
            field=models.ForeignKey(to='cannula.region'),
        ),
        migrations.AddField(
            model_name='district',
            name='roid',
            field=models.ForeignKey(to='cannula.region'),
        ),
    ]
