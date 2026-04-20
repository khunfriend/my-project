from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_plant_price_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='plants/'),
        ),
    ]
