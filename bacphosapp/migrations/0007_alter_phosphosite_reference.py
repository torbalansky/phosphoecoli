# Generated by Django 5.0.2 on 2024-03-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacphosapp', '0006_phosphoprotein_biological_process_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phosphosite',
            name='reference',
            field=models.CharField(default=''),
        ),
    ]