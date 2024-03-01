# Generated by Django 5.0.2 on 2024-03-01 11:45

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bacphosapp', '0003_remove_phosphoprotein_alphafold_link_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phosphoprotein',
            name='modification_type',
        ),
        migrations.RemoveField(
            model_name='phosphoprotein',
            name='position',
        ),
        migrations.RemoveField(
            model_name='phosphoprotein',
            name='sequence',
        ),
        migrations.RemoveField(
            model_name='phosphoprotein',
            name='window_5_aa',
        ),
        migrations.AddField(
            model_name='phosphoprotein',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='phosphoprotein',
            name='submitted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PhosphoSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('window_5_aa', models.TextField()),
                ('sequence', models.TextField()),
                ('modification_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('protein', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bacphosapp.phosphoprotein')),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]