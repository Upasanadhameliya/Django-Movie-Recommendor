from moviedisp.models import Movie
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from imdb import IMDb
from PIL import Image
import requests
from io import BytesIO

def get_movies():
	ia = IMDb()
	movies = ia.get_top250_movies()

	for i,movie in enumerate(movies):
		# if i < 25:
		# 	add_movie(movie,ia)
		# else:
		# 	break
		add_movie(movie,ia)

def add_movie(movie,ia):
	IMAGE_WIDTH = 182
	IMAGE_HEIGHT = 268
	movie = ia.search_movie(str(movie['title']))[0]
	sr_title = movie['title'][:25]
	ln_title = movie['long imdb title']
	title = movie['title']
	yr = str(movie['year'])

	movie_obj = Movie(title = title,short_title=sr_title,long_title=ln_title,year = yr)
	img_field = movie_obj.image
	print(movie['title'])

	resp = requests.get(movie['full-size cover url'])
	pillow_image = Image.open(BytesIO(resp.content))
	img_name= str(movie['title']) + ".jpg"

	img = resize_image(pillow_image,width=IMAGE_WIDTH,
                  height=IMAGE_HEIGHT)

	img_field.save(img_name, InMemoryUploadedFile(img,None,img_name,'image/jpeg',img.tell,None))
	movie_obj.save()

def resize_image(img, width, height):
	if img.size[0] > width or img.size[1] > height:
		new_image = img.resize((width,height))

	buffer = BytesIO()
	new_image.save(fp=buffer,format='JPEG')
	return ContentFile(buffer.getvalue())
