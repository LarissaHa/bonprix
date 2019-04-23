from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Product, Topic
from django.utils import timezone
from .forms import ReviewForm, ReviewFormUnknown
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def review_list(request):
    reviews = Review.objects.filter(date__lte=timezone.now()).order_by('-date')
    reviews, page = paginator_spec(request, reviews)
    return render(request, 'reviews/review_list.html', {'reviews': reviews, 'page': page})

def index(request):
    return render(request, 'reviews/home.html', {})

def product_list(request):
    products = Product.objects.filter().order_by('number')
    return render(request, 'reviews/product_list.html', {'products': products})

def paginator_spec(request, review_list):
    # PAGINATOR
    paginator = Paginator(review_list, 10)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    return reviews, page

def star_generator(review_list):
    # STARS AND RATING GENERATOR
    average = 0
    rating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    if len(review_list) > 0:
        for review in review_list:
            average = average + int(review.stars)
        average = average / len(review_list)
        average = round(average, 1)
        for review in review_list:
            for i in range(1,6):
                if int(review.stars) == i:
                    rating[str(i)] = rating[str(i)] + 1
        for stars in rating:
            rating[stars] = ( rating[stars] / len(review_list) ) * 100
            rating[stars] = round(rating[stars], 1)
    return average, rating

def product_detail(request, pk):
    products = get_object_or_404(Product, pk=pk)

    # CALL REVIEWS
    review_list = Review.objects.filter(date__lte=timezone.now()).filter(product_number=pk)

    # TOPICS GENERATOR
    topics_complicated = Topic.objects.filter(product=pk)
    topics = topics_complicated.values('topic', 'topic_safe').annotate(freq_topic=Count('topic')).order_by('-freq_topic')[:10]
    topics_list = list()
    topics_number = list()
    topics_safe = list()
    for item in list(topics):
        topics_list.append(item["topic"])
        topics_number.append(item["freq_topic"])
        topics_safe.append(item["topic_safe"])

    average, rating = star_generator(review_list)

    # CALL PRODUCT
    products = Product.objects.filter(pk=pk).order_by('number')
    return review_list, products, average, rating, topics_list, topics_number, topics_safe, topics

def product_detail_star(request, pk, star):
    review_list, products, average, rating, topics_list, topics_number, topics_safe, topics = product_detail(request, pk)
    review_list = review_list.filter(stars=star).order_by('-date')
    # paginator = Paginator(review_list, 10)
    # page = request.GET.get('page')
    # try:
    #     reviews = paginator.page(page)
    # except PageNotAnInteger:
    #     reviews = paginator.page(1)
    # except EmptyPage:
    #     reviews = paginator.page(paginator.num_pages)
    reviews, page = paginator_spec(request, review_list)
    return render(request, 'reviews/product_detail_star.html', {'reviews': reviews, 'products': products, 'average': average, 'rating': rating, 'topics_list': topics_list, 'topics_number': topics_number, 'topics_safe': topics_safe, 'topics': topics, 'page': page, 'star': star})


def product_detail_sort(request, pk, sort):
    review_list, products, average, rating, topics_list, topics_number, topics_safe, topics = product_detail(request, pk)
    if sort == "pos":
        review_list = review_list.order_by('-stars')
        tag = "Positive"
    elif sort == "neg":
        review_list = review_list.order_by('stars')
        tag = "Negative"
    else:
        review_list = review_list.order_by('-date')
        tag = "Neueste"
    reviews, page = paginator_spec(request, review_list)
    return render(request, 'reviews/product_detail_sort.html', {'reviews': reviews, 'products': products, 'average': average, 'rating': rating, 'topics_list': topics_list, 'topics_number': topics_number, 'topics_safe': topics_safe, 'topics': topics, 'page': page, 'tag': tag})


def product_detail_topic(request, pk, topic_safe):
    review_list, products, average, rating, topics_list, topics_number, topics_safe, topics = product_detail(request, pk)
    topic_with_product = Topic.objects.filter(product=pk, topic_safe=topic_safe).values('review').order_by('review')
    id_list = [ids['review'] for ids in topic_with_product]
    reviews_with_topic = Review.objects.filter(product_number=pk, pk__in=id_list)
    reviews, page = paginator_spec(request, reviews_with_topic)
    topic_average, topic_rating = star_generator(reviews)
    return render(request, 'reviews/product_detail_topic.html', {'reviews': reviews, 'products': products, 'average': average, 'rating': rating, 'topics_list': topics_list, 'topics_number': topics_number, 'topics_safe': topics_safe, 'page': page, 'topic_safe': topic_safe, 'topics': topics, 'topic_average': topic_average})


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
            # for t in range(len(topic[0])):
            #     top = Topic(review=review.pk, product=Product.objects.filter(pk=product)[0], topic=topic[0][t], topic_safe=[1][t])
            #     top.save()
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
            review.save()
            # for t in range(len(topic[0])):
            #     top = Topic(review=review.pk, product=Product.objects.filter(pk=product)[0], topic=topic[0][t], topic_safe=[1][t])
            #     top.save()
            return redirect('product_detail', pk=review.product_number.number)
    else:
        form = ReviewFormUnknown()
    return render(request, 'reviews/review_new_unknown.html', {'form': form})
    