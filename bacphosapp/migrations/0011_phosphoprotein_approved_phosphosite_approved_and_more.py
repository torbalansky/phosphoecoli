# Generated by Django 5.0.2 on 2024-03-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacphosapp', '0010_phosphoprotein_ecocyc_url_phosphoprotein_pdb_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='phosphoprotein',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phosphosite',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
