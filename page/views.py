from django.shortcuts import render, redirect
from . import forms
from RateMyRetail.GoogleMapsClient import GoogleMapsClient
from RateMyRetail import settings

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
    searchClient = GoogleMapsClient(settings.GOOGLE_MAPS_API_KEY)
    data = searchClient.getByPlaceID(params)
    data['key'] = settings.GOOGLE_MAPS_API_KEY
    return render(request,'page/view.html', data)