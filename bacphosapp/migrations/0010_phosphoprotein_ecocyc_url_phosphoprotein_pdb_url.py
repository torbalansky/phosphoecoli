# Generated by Django 5.0.2 on 2024-03-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacphosapp', '0009_remove_phosphosite_references_phosphosite_reference_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='phosphoprotein',
            name='ecocyc_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='phosphoprotein',
            name='pdb_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
