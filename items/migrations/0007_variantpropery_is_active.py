# Generated by Django 2.1.5 on 2019-01-25 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20190125_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='variantpropery',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
