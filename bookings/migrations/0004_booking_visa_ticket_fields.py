from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='visa_status',
            field=models.CharField(blank=True, choices=[('not_applied', 'Not Applied'), ('applied', 'Applied'), ('in_review', 'In Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='not_applied', max_length=20),
        ),
        migrations.AddField(
            model_name='booking',
            name='visa_expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='visa_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='pnr_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='airline',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='flight_from',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='flight_to',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='ticket_status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('issued', 'Issued'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='booking',
            name='ticket_class',
            field=models.CharField(blank=True, choices=[('economy', 'Economy'), ('business', 'Business'), ('first', 'First Class')], default='economy', max_length=20),
        ),
    ]
