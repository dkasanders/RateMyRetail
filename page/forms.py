#All form class data

from django import forms
from django.utils import timezone
import datetime




class SearchForm(forms.Form):
    search_text = forms.CharField(label="Search")
    search_location = forms.CharField(label="Location")


class ReviewForm(forms.Form):
    EMPLOYMENT_CHOICES = [
        ('part_time', 'Part Time'),
        ('full_time', 'Full Time')
    ]
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent')
    ]

    position_title = forms.CharField(
        label='Position Title'
    )

    employment_type = forms.ChoiceField(
        label="Employment Type",
        widget=forms.RadioSelect,
        choices=EMPLOYMENT_CHOICES
    )

    employment_start = forms.CharField(
        widget=forms.DateInput(attrs={'type': 'month'})
    )
    employment_end = forms.CharField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        required=False
    )



    currently_employed = forms.BooleanField(
        label="I currently work here",
        required=False
    )
    flexibility_rating = forms.ChoiceField(
        label="I feel my employer offered a flexible schedule:",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'})
    )

    benefits_rating = forms.ChoiceField(
        label="I feel my employer offered meaningful employee benefits (401K, PTO, etc.):",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'})
    )

    compensation_rating = forms.ChoiceField(
        label="I feel my employer compensated me fairly for the work I did:",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'})
    )

    overall_rating = forms.ChoiceField(
        label="Overall, I am satisifed with my workplace and employer:",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'})
    )

    review_text = forms.CharField(
        label="Write a Review:",
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40})
    )

    def validateMonthYear(self, monthYear):
        Values = monthYear.split('-')
        current_year = timezone.now().year
        current_month = timezone.now().month

        if(int(Values[0]) > current_year):
            return False
        if(int(Values[0]) == current_year and int(Values[1]) >  current_month):
            return False
        if(int(Values[1]) > 12 and int(Values[1]) < 1):
            return False
        return True

    #With a list of month year params, validates the starting date isnt after the ending date.
    def validateStartEnd(self, monthYears):
        startDate = monthYears[0]
        endDate = monthYears[1]

        if(int(startDate[0]) > int(endDate[0])):
            return False
        if(int(startDate[0]) == int(endDate[0])  and int(startDate[1]) > int(endDate[1])):
            return False
        return True


    def clean(self):
        cleaned_data = super().clean()

        #Form Values
        employment_type = cleaned_data.get('employment_type')
        employment_start = cleaned_data.get('employment_start')
        employment_end = cleaned_data.get('employment_end')
        currently_employed = cleaned_data.get('currently_employed')
        flexibility_rating = cleaned_data.get('flexibility_rating')
        benefits_rating = cleaned_data.get('benefits_rating')
        compensation_rating = cleaned_data.get('compensation_rating')
        overall_rating = cleaned_data.get('overall_rating')
        review_text = cleaned_data.get('review_text')

        ratings = [flexibility_rating, benefits_rating, compensation_rating, overall_rating]

        if (employment_type != 'part_time' and employment_type != 'full_time'):
            self.add_error('employment_type', 'Invalid Value. ' + employment_type + ' given.')
        if(self.validateMonthYear(employment_start) == False):
            self.add_error('employment_start', 'Invalid Value. ' + employment_start + ' given.')


        if(employment_end == ''):
            if(currently_employed == False):
                self.add_error('employment_end', 'No value given or currently_employed is not true.')
        else:
            if(currently_employed):
                self.add_error('employment_end', 'End date given despite currently_employed being true.')
            if(self.validateMonthYear(employment_end) == False):
                self.add_error('employment_end', 'Invalid Value. ' + employment_end + ' given.')
            if(self.validateStartEnd([employment_start.split('-'), employment_end.split('-')]) == False):
                self.add_error('employment_start', 'Employment start date is after the employment end date')


        for rating in ratings:
            if(int(rating) < 1 or int(rating) > 5):
                self.add_error('rating', 'Invalid rating given. Ratings are between 1-5.')

        if(review_text == ''):
            self.add_error('review_text', 'Review text needs to be given')


        return cleaned_data
