from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import auth
from .models import Movie
from django.core.paginator import Paginator
from imdb import IMDb
from django.forms.models import model_to_dict
import pickle
import pandas as pd


def home_page(request,pageno=1):
	template = loader.get_template('moviedisp/home.html')
	startpage = None

	new_obj = Movie.objects.all().filter(top_movie=True).order_by('-year')
	paginator = Paginator(new_obj, 24)
	no_of_pages = paginator.num_pages
	if pageno < (no_of_pages-4):
		startpage = pageno
	else:
		startpage = (no_of_pages-4)

	endpage = startpage + 5
	pagelist = [i for i in range(startpage,endpage)]

	page_obj = paginator.get_page(pageno)
	context = {"movies":page_obj,"pg":pagelist,"prev":startpage-1,"next":endpage+1}

	return HttpResponse(template.render({"context":context},request))

def logout(request):
	auth.logout(request)
	return redirect('/')



def content_based(request,pageno=1):
	template = loader.get_template('moviedisp/genres.html')
	new_obj = Movie.objects.all().filter(top_movie=False)

	for movie in new_obj:
		movie.range = range(movie.ratings)
		movie.white_star = range(4-movie.ratings)

	paginator = Paginator(new_obj, 24)
	no_of_pages = paginator.num_pages

	startpage = None

	if pageno < (no_of_pages-4):
		startpage = pageno
	else:
		startpage = (no_of_pages-4)

	endpage = startpage + 5
	pagelist = [i for i in range(startpage,endpage)]

	page_obj = paginator.get_page(pageno)
	context = {"movies":page_obj,"pg":pagelist,"prev":startpage-1,"next":endpage+1}

	return HttpResponse(template.render({"context":context},request))



def related(request,movie_id=-1):
	template = loader.get_template('moviedisp/related.html')
	# new_obj = Movie.objects.all().filter(top_movie=False)[:20]

	new_obj = return_related_movies(movie_id)
	for movie in new_obj:
		movie.range = range(movie.ratings)
		movie.white_star = range(4-movie.ratings)
	# return HttpResponse("Related!")
	return HttpResponse(template.render({"movies":new_obj},request))


def return_related_movies(movie_id):
	with open("modelfile.sav","rb") as f:
		cosine_sim = pickle.load(f)
	new_obj = Movie.objects.all().filter(top_movie=False)
	movie_list = []
	index_list = []
	for index,movie in enumerate(new_obj):
		movie_list.append(movie.id)
		index_list.append(index)

	indices = pd.Series(index_list,index=movie_list)
	print(indices.head(n=20))
	idx = indices[movie_id]
	sim_scores = list(enumerate(cosine_sim[idx]))
	sim_scores = sorted(sim_scores,key=lambda x: x[1],reverse=True)[1:25]
	match_index = [i[0] for i in sim_scores]
	print(match_index)
	movies = []
	for index,movie in enumerate(new_obj):
		if index in match_index:
			movies.append(movie)

	return movies

# from django.core.files.base import ContentFile
# from django.core.files.uploadedfile import InMemoryUploadedFile

# from imdb import IMDb
# from PIL import Image
# import requests
# from io import BytesIO


# Create your views here.
# def home_page(request):
# 	IMAGE_WIDTH = 182
# 	IMAGE_HEIGHT = 268
	# ia = IMDb()
	# movies = ia.search_movie('Shrek (2001)')
	# sr_title = movies[0]['title']
	# ln_title = movies[0]['long imdb title']
	# yr = str(movies[0]['year'])

	# movie_obj = Movie(short_title=sr_title,long_title=ln_title,year = yr)
	# img_field = movie_obj.image

	# resp = requests.get(movies[0]['full-size cover url'])
	# pillow_image = Image.open(BytesIO(resp.content))
	# img_name="toy_story.jpg"

	# img = resize_image(pillow_image,width=IMAGE_WIDTH,
 #                  height=IMAGE_HEIGHT)

	# img_field.save(img_name, InMemoryUploadedFile(img,None,img_name,'image/jpeg',img.tell,None))
	# movie_obj.save()

	# template = loader.get_template('moviedisp/genres.html')
	# new_obj = Movie.objects.all()

	# return HttpResponse(template.render({"movies":new_obj},request))

# def resize_image(img, width, height):
# 	if img.size[0] > width or img.size[1] > height:
# 		new_image = img.resize((width,height))

# 	buffer = BytesIO()
# 	new_image.save(fp=buffer,format='JPEG')
# 	return ContentFile(buffer.getvalue())


# new_obj = Movie.objects.all()
	# ia = IMDb()

	# for each in new_obj:
	# 	if each.title == "":
	# 		if each.long_title is not None and each.short_title is not "Rush":
	# 			movie = ia.search_movie(str(each.long_title))
	# 			movie = movie[0]
	# 			each.title = movie['title']
	# 			each.save()
	# 	else:
	# 		continue
