from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0004_agency_invoice_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='advanced_features_enabled',
            field=models.BooleanField(default=False, help_text='Enable advanced features (Visa & Ticket management) for this agency'),
        ),
    ]
