# Generated by Django 3.1.7 on 2021-12-20 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20211213_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(blank=True, max_length=20, null=True)),
                ('rank', models.CharField(blank=True, max_length=20, null=True)),
                ('bdate', models.TextField(blank=True, null=True)),
                ('rtp', models.IntegerField(blank=True, db_column='RTP', null=True)),
                ('passdate', models.TextField(blank=True, null=True)),
                ('attvalid', models.IntegerField(blank=True, null=True)),
                ('why', models.TextField(blank=True, null=True)),
                ('document', models.TextField(blank=True, null=True)),
                ('getdate', models.TextField(blank=True, null=True)),
                ('findate', models.TextField(blank=True, null=True)),
                ('gdzs', models.TextField(blank=True, db_column='GDZS', null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['fullname'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='attvalid',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='bdate',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='document',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='findate',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='gdzs',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='getdate',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='passdate',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='post',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='rtp',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='why',
        ),
        migrations.AddField(
            model_name='customuser',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.person'),
        ),
    ]
