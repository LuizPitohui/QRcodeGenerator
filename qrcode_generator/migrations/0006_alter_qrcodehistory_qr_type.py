# Generated by Django 5.2.4 on 2025-07-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcode_generator', '0005_remove_qrcodehistory_expires_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcodehistory',
            name='qr_type',
            field=models.CharField(choices=[('text', 'Texto'), ('url', 'URL'), ('pdf', 'PDF'), ('email', 'Email'), ('phone', 'Telefone'), ('sms', 'SMS'), ('wifi', 'WiFi'), ('vcard', 'vCard')], default='text', max_length=10, verbose_name='Tipo'),
        ),
    ]
