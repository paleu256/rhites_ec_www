# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cannula', '0027_auto_20230425_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='roid',
            field=models.ForeignKey(related_name='district', to='cannula.region'),
        ),
        migrations.AlterField(
            model_name='health_facility',
            name='doid',
            field=models.ForeignKey(related_name='healthfacility', to='cannula.district'),
        ),
        migrations.AlterField(
            model_name='health_subcounty',
            name='hfoid',
            field=models.ForeignKey(related_name='subcounty', to='cannula.health_facility'),
        ),
    ]
