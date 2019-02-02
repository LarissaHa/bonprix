# Generated by Django 2.0.10 on 2019-02-02 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20190202_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(default='', upload_to='reviews/static/images/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='product_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Product'),
        ),
    ]