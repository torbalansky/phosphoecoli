# Generated by Django 5.0.2 on 2024-03-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacphosapp', '0013_remove_phosphoprotein_alphafold_structure_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='phosphoprotein',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
