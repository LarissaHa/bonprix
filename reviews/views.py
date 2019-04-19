from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Product, Topic
from django.utils import timezone
from .forms import ReviewForm, ReviewFormUnknown
import pandas as pd

# Create your views here.
def review_list(request):
    reviews = Review.objects.filter(date__lte=timezone.now()).order_by('-date')
    return render(request, 'reviews/review_list.html', {'reviews': reviews[:5]})

def index(request):
    return render(request, 'reviews/home.html', {})

def product_list(request):
    products = Product.objects.filter().order_by('number')
    return render(request, 'reviews/product_list.html', {'products': products})

def product_detail(request, pk):
    #reviews = get_object_or_404(Review, pk=pk)
    reviews = Review.objects.filter(date__lte=timezone.now()).filter(product_number=pk).order_by('-date')
    topics = list()
    topics_complicated = Topic.objects.filter(product=pk)
    for g in range(len(topics_complicated)):
        topics.append(topics_complicated[g].topic)
    #display_topics = Topic.objects.filter(product=pk).distinct('topic')
    comparison = pd.DataFrame(columns=['freq'], index=set(topics))
    comparison = comparison.fillna(0)
    for g in topics:
        comparison["freq"][g] += 1
    comparison = comparison.sort_values("freq", ascending=False).head(10)
    topics_list = comparison.index.tolist()
    topics_number = comparison.freq.tolist()

    average = 0
    rating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    if len(reviews) > 0:
        for review in reviews:
            average = average + int(review.stars)
        average = average / len(reviews)
        average = round(average, 1)
        for review in reviews:
            for i in range(1,6):
                if int(review.stars) == i:
                    rating[str(i)] = rating[str(i)] + 1
        for stars in rating:
            rating[stars] = ( rating[stars] / len(reviews) ) * 100
            rating[stars] = round(rating[stars], 1)
    products = Product.objects.filter(pk=pk).order_by('number')
    return render(request, 'reviews/product_detail.html', {'reviews': reviews, 'products': products, 'average': average, 'rating': rating, 'topics_list': topics_list, 'topics_number': topics_number})

def review_new(request, product):
    products = Product.objects.filter(pk=product).order_by('number')
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = "Unknown"
            review.date = timezone.now()
            review.product_number = Product.objects.filter(pk=product)[0]
            review.save()
            return redirect('product_detail', pk=product)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_edit.html', {'form': form, 'products': products})
    #return redirect('reviews/review_edit.html', {'form': form, 'pk': product})

def review_new_unknown(request):
    #products = Product.objects.filter(pk=product).order_by('number')
    if request.method == "POST":
        form = ReviewFormUnknown(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = "Unknown"
            review.date = timezone.now()
            #review.product_number = Product.objects.filter(pk=product)[0]
            review.save()
            return redirect('product_detail', pk=review.product_number.number)
    else:
        form = ReviewFormUnknown()
    return render(request, 'reviews/review_new_unknown.html', {'form': form})
    