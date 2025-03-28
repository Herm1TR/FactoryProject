# Generated by Django 5.1.7 on 2025-03-21 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location_x', models.FloatField(help_text='X 軸座標')),
                ('location_y', models.FloatField(help_text='Y 軸座標')),
                ('current_load', models.IntegerField(default=0, help_text='當前載重')),
                ('max_capacity', models.IntegerField(help_text='最大載重容量')),
            ],
        ),
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50, unique=True)),
                ('current_x', models.FloatField(help_text='當前 X 座標')),
                ('current_y', models.FloatField(help_text='當前 Y 座標')),
                ('is_active', models.BooleanField(default=True, help_text='是否啟動中')),
            ],
        ),
        migrations.CreateModel(
            name='LogisticsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('route_taken', models.TextField(help_text='機器人運送路徑紀錄（例如：座標序列）')),
                ('load_delivered', models.IntegerField(help_text='送貨量')),
                ('dock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.dock')),
                ('robot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.robot')),
            ],
        ),
    ]
