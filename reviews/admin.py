from django.contrib import admin
from .models import Review, Product, Topic
# Register your models here.

admin.site.register(Review)
admin.site.register(Product)
admin.site.register(Topic)