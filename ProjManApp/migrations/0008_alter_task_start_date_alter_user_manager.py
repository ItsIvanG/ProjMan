# Generated by Django 4.2.17 on 2024-12-16 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProjManApp', '0007_remove_file_manager_id_alter_file_share_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='manager',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'Manager'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]