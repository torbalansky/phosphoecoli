# Generated by Django 5.0.2 on 2024-03-02 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacphosapp', '0008_reference_remove_phosphosite_reference_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phosphosite',
            name='references',
        ),
        migrations.AddField(
            model_name='phosphosite',
            name='reference',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='Reference',
        ),
    ]
