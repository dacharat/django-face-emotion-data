# Generated by Django 2.2.2 on 2019-07-12 10:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0007_auto_20190712_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testperson',
            name='face_encodong',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default={'a': 0}, size=None),
        ),
    ]