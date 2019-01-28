from django.shortcuts import render
from .models import Post
from django.utils import timezone

# Create your views here.
def review_list(request):
    reviews = Review.objects.filter(date__lte=timezone.now()).order_by('date')
    return render(request, 'blog/review_list.html', {'reviews': reviews})

def reviews_detail(request, product):
    reviews = Review.objects.filter(date__lte=timezone.now()).filter_by(product_number=product).order_by('date')