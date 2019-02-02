from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Product
from django.utils import timezone
from .forms import ReviewForm

# Create your views here.
def review_list(request):
    reviews = Review.objects.filter(date__lte=timezone.now()).order_by('date')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def index(request):
    return render(request, 'reviews/index.html', {})

def product_list(request):
    products = Product.objects.filter().order_by('number')
    return render(request, 'reviews/product_list.html', {'products': products})

def product_detail(request, pk):
    #reviews = get_object_or_404(Review, pk=pk)
    reviews = Review.objects.filter(date__lte=timezone.now()).filter(product_number=pk).order_by('date')
    products = Product.objects.filter(pk=pk).order_by('number')
    return render(request, 'reviews/product_detail.html', {'reviews': reviews, 'products': products})

def review_new(request, product):
    products = Product.objects.filter(pk=product).order_by('number')
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            #review.author = request.user
            review.date = timezone.now()
            review.product_number = Product.objects.filter(pk=product)[0]
            review.save()
            return redirect('product_detail', pk=product)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_edit.html', {'form': form, 'products': products})
    #return redirect('reviews/review_edit.html', {'form': form, 'pk': product})
    