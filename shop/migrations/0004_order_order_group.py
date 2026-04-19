from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_plant_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_group',
            field=models.UUIDField(blank=True, db_index=True, null=True),
        ),
    ]
