# Generated by Django 2.1.5 on 2019-01-25 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_itemchangelog_variantchangelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='last_user',
            field=models.CharField(default='admin', max_length=255),
        ),
        migrations.AddField(
            model_name='variant',
            name='last_user',
            field=models.CharField(default='admin', max_length=255),
        ),
        migrations.AddField(
            model_name='variantpropery',
            name='last_user',
            field=models.CharField(default='admin', max_length=255),
        ),
    ]
