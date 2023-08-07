from django.shortcuts import render, redirect
from . import forms
from RateMyRetail.GoogleMapsClient import GoogleMapsClient
from RateMyRetail import settings
from django.http import HttpResponse
from django.utils import timezone
from .models import Review, Location
from django.contrib import admin
from django.core import serializers

# Create your views here.


def home(request):
    if request.method == "POST":
        formData = forms.SearchForm(request.POST)
        if formData.is_valid():
           query = formData.cleaned_data['search_text'] + '&' + formData.cleaned_data['search_location']
           return redirect('page-search', params=query)

    return render(request, 'page/home.html', {'form' : forms.SearchForm()})


def search(request, params):
    listParams = params.split('&')
    searchClient = GoogleMapsClient(settings.GOOGLE_MAPS_API_KEY)
    searchReturn = searchClient.searchResponse(listParams)
    return render(request, 'page/search.html', searchReturn)


def view(request, params):
    if(params == 'admin'):
        return redirect('admin:index')
    searchClient = GoogleMapsClient(settings.GOOGLE_MAPS_API_KEY)
    data = searchClient.getByPlaceID(params)
    data['key'] = settings.GOOGLE_MAPS_API_KEY
    if(Location.objects.filter(maps_id=params).exists()):
        l = Location.objects.get(maps_id=params)
        data['averages'] = l.review_averages
        review_count = l.reviews.count()
        if review_count == 1:
            data['total_reviews'] = "1 Review"
        else:
            data['total_reviews'] = str(review_count) + " Reviews"
        reviewsData = l.reviews.all()
        reviews = list(reviewsData.values())
        cleanedReviews = []
        for review in reviews:
            del review['user_ip']
            cleanedReviews.append(review)
        data['reviews'] = cleanedReviews


    return render(request,'page/view.html', data)


def review(request, id):
    searchClient = GoogleMapsClient(settings.GOOGLE_MAPS_API_KEY)
    data = searchClient.getByPlaceID(id)
    data['form'] = forms.ReviewForm()

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data

            review_instance = Review.objects.create(
                position_title = formData['position_title'],
                employment_type = formData['employment_type'],
                employment_start= formData['employment_start'],
                employment_end = formData['employment_end'],
                currently_employed = formData['currently_employed'],
                flexibility_rating = formData['flexibility_rating'],
                benefits_rating = formData['benefits_rating'],
                compensation_rating = formData['compensation_rating'],
                overall_rating = formData['overall_rating'],
                review_text = formData['review_text'],
                user_ip = request.META.get('REMOTE_ADDR', '')
            )

            if Location.objects.filter(maps_id=id).exists():
                #If true review for location has already been made.
                l = Location.objects.get(maps_id=id)
                oldTotalReviews = l.review_count
                l.review_count = l.review_count + 1

                #Updating averages
                averageTable = l.review_averages
                averageTable['flexibility']  = (int(averageTable['flexibility'])  * oldTotalReviews + int(formData['flexibility_rating']))  / (oldTotalReviews + 1)
                averageTable['benefits']     = (int(averageTable['benefits'])     * oldTotalReviews + int(formData['benefits_rating']))     / (oldTotalReviews + 1)
                averageTable['compensation'] = (int(averageTable['compensation']) * oldTotalReviews + int(formData['compensation_rating'])) / (oldTotalReviews + 1)
                averageTable['overall']      = (int(averageTable['overall'])      * oldTotalReviews + int(formData['overall_rating']))      / (oldTotalReviews + 1)
                l.review_averages = averageTable

                l.save()
                l.reviews.add(review_instance)
            else:
                location_instance = Location.objects.create(
                    name = data['name'],
                    maps_id=id,
                    formatted_address = data['formatted_address'],
                    review_count = 1,
                    review_averages = {
                        'flexibility': formData['flexibility_rating'],
                        'benefits': formData['benefits_rating'],
                        'compensation': formData['compensation_rating'],
                        'overall': formData['overall_rating']
                    }


                )
                location_instance.reviews.add(review_instance)

            return redirect('page-home')
        else:
            print(form.errors)
            print(form.cleaned_data)
            return HttpResponse(str(form.errors))

    else:
        return render(request, 'page/review.html', data)