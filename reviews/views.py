from django.shortcuts import render
from .models import Review
from django.utils import timezone

# Create your views here.
def review_list(request):
    reviews = Review.objects.filter(date__lte=timezone.now()).order_by('date')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def index(request):
    return render(request, 'reviews/index.html', {})

def reviews_detail(request, product):
    reviews = Review.objects.filter(date__lte=timezone.now()).filter_by(product_number=product).order_by('date')