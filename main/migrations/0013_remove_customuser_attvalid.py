# Generated by Django 3.1.7 on 2022-01-02 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20220102_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='attvalid',
        ),
    ]
