# Generated by Django 3.1.7 on 2022-01-02 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20220102_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attvalid',
            options={'verbose_name': 'Вид аттестации', 'verbose_name_plural': 'Виды аттестации'},
        ),
        migrations.AlterModelTable(
            name='attvalid',
            table=None,
        ),
    ]
