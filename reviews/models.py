from django.db import models
 
# Create your models here.
from django.conf import settings 
from django.db import models 
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    STARS = (("1", "X"), ("2", "XX"), ("3", "XXX"), ("4", "XXXX"), ("5", "XXXXX"))
    author = models.TextField("Name des Kunden", max_length=30)
    text = models.TextField("Ausführliche Bewertung")
    date = models.DateTimeField(
            default=timezone.now)
    stars = models.CharField("Sterne",
        max_length=1, choices=STARS)
    product_number = models.ForeignKey('product', on_delete=models.PROTECT)

class Product(models.Model):
    number = models.IntegerField("Produkt Nummer", primary_key=True)
    name = models.TextField("Name des Produktes")
    picture = models.ImageField(upload_to = 'reviews/static/images/', default='')
    star1_count = models.IntegerField(default=0)
    star2_count = models.IntegerField(default=0)
    star3_count = models.IntegerField(default=0)
    star4_count = models.IntegerField(default=0)
    star5_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Topic(models.Model):
    review = models.ForeignKey('review', on_delete=models.PROTECT)
    product = models.ForeignKey('product', on_delete=models.PROTECT, default=0)
    topic = models.TextField("Kategorie des Inhalts", max_length=30)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title