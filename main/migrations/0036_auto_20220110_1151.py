# Generated by Django 3.1.7 on 2022-01-10 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20220109_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='attvalid',
            new_name='approvals',
        ),
    ]