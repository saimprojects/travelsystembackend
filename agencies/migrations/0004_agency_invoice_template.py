from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0003_agency_address_agency_description_agency_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='invoice_template',
            field=models.CharField(
                choices=[
                    ('classic', 'Classic Blue'),
                    ('gold_voucher', 'Gold Voucher'),
                    ('dark_pro', 'Dark Professional'),
                    ('minimal', 'Modern Minimal'),
                    ('corporate', 'Corporate'),
                ],
                default='classic',
                max_length=20,
            ),
        ),
    ]
