# Generated by Django 4.2.17 on 2024-12-15 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjManApp', '0004_alter_file_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='filename',
            field=models.FileField(upload_to='uploaded_files/'),
        ),
    ]
