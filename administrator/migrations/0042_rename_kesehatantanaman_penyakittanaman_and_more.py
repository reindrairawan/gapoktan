# Generated by Django 5.1.6 on 2025-07-15 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0041_rename_kondisi_kesehatantanaman_penyakit_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KesehatanTanaman',
            new_name='PenyakitTanaman',
        ),
        migrations.AlterModelOptions(
            name='penyakittanaman',
            options={'verbose_name_plural': 'Data Penyakit Tanaman'},
        ),
    ]
