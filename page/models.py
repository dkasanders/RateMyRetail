from django.db import models
import datetime
# Create your models here.

class Review(models.Model):
    position_title = models.CharField(max_length=500)
    employment_type = models.CharField(max_length=9)
    employment_start = models.CharField(max_length=7)
    employment_end = models.CharField(max_length=7)
    currently_employed = models.BooleanField()
    flexibility_rating = models.IntegerField()
    benefits_rating = models.IntegerField()
    compensation_rating = models.IntegerField()
    overall_rating = models.IntegerField()
    review_text = models.TextField()
    date_posted = models.DateTimeField(default=datetime.datetime.now)
    user_ip = models.GenericIPAddressField(protocol='IPv4')


    def __str__(self):
        return self.position_title





class Location(models.Model):
    name = models.CharField(max_length=500)
    maps_id = models.CharField(max_length=500)
    formatted_address = models.CharField(max_length=1000)

    review_averages = models.JSONField(default={
        'flexibility': 'N/A',
        'benefits': 'N/A',
        'compensation': 'N/A',
        'overall': 'N/A'
    })

    reviews = models.ManyToManyField(Review)

    def __str__(self):
        return self.name

