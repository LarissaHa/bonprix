# Generated by Django 2.0.10 on 2019-02-02 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20190131_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='picture',
            field=models.FileField(default='', upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='product_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Product'),
        ),
    ]
