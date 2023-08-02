#All form class data

from django import forms

class SearchForm(forms.Form):
    search_text = forms.CharField(label="Search")
    search_location = forms.CharField(label="Location")

