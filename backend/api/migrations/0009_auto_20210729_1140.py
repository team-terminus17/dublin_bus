# Generated by Django 3.2.4 on 2021-07-29 10:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_routestops_shape'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceexceptions',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Realtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('delay', models.IntegerField()),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stops')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.trips')),
            ],
        ),
    ]