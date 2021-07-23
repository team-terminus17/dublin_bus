# Generated by Django 3.2.4 on 2021-07-20 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_stops_routes_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='clamt',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='weather',
            name='vis',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='weather',
            name='wdsp',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='weather',
            name='rain',
            field=models.FloatField(),
        ),
    ]