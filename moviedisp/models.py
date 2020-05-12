from django.db import models

# Create your models here.

class Movie(models.Model):
	title = models.CharField(max_length=150,default="")
	short_title = models.CharField(max_length=25)
	long_title = models.CharField(max_length=200)
	year = models.CharField(max_length=4)
	image = models.ImageField(upload_to='movieimg')
	ratings = models.IntegerField(default=4)
	half_rating = models.BooleanField(default=False)
	top_movie = models.BooleanField(default=True)
	genres = models.CharField(max_length=200,default="")

	def __str__(self):
		return self.title
