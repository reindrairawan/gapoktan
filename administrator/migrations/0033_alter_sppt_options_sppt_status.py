# Generated by Django 5.1.6 on 2025-06-16 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0032_sppt_nama_petani'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sppt',
            options={'verbose_name_plural': 'Data Sppt'},
        ),
        migrations.AddField(
            model_name='sppt',
            name='status',
            field=models.CharField(choices=[('proses', 'Diproses'), ('diterima', 'Diterima'), ('ditolak', 'Ditolak')], default='proses', max_length=20),
        ),
    ]
