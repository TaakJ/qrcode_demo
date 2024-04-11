# Generated by Django 4.2.11 on 2024-04-08 03:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apps_home", "0007_alter_library_qr_code"),
    ]

    operations = [
        migrations.DeleteModel(
            name="library",
        ),
        migrations.RemoveField(
            model_name="company_profile",
            name="dual_date",
        ),
        migrations.AlterField(
            model_name="company_qrcode",
            name="qr_code",
            field=models.ImageField(blank=True, upload_to="qr_codes"),
        ),
    ]
