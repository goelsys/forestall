# Generated by Django 5.1.2 on 2024-10-31 17:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0005_risk_first_indicator_risk_reason_and_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='prj',
            name='status',
            field=models.CharField(blank=True, choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Closed', 'Closed'), ('OnHold', 'OnHold')], max_length=20),
        ),
        migrations.AlterField(
            model_name='risk',
            name='date_identified',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='risk',
            name='date_last_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
