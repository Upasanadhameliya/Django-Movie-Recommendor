from moviedisp.models import Movie
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
import os

from imdb import IMDb
from PIL import Image
import requests
from io import BytesIO

def get_movies():
	ia = IMDb()
	filepath = "S:/Sandy/Documents/College/Practice/AI/Movielens Recommendor/"

	movies_df = pd.read_csv(os.path.join(filepath,"movies.csv"),sep="\t",encoding="latin_1",engine="python")
	print("Dataframe created!")

	ratings_df = pd.read_csv(os.path.join(filepath,"ratings.csv"),usecols=['movie_id','rating'],sep="\t",encoding="latin_1",engine="python")
	print("Dataframe created!")

	dataset = ratings_df.merge(movies_df,how='outer')
	dataset_new = dataset.groupby('title').mean()['rating']

	ds_new = pd.DataFrame(data={"rating":dataset_new.values,"title":dataset_new.index})

	mean_val = round(ds_new['rating'].mean(),1)
	ds_new['rating'].fillna(mean_val,inplace=True)
	ds_new['rating'] = ds_new['rating'].apply(lambda x: round(x,1))

	movies_df = movies_df.merge(ds_new,how='outer',on='title')

	movies_df['genres'] = movies_df['genres'].fillna("").astype(str)
	movies_df['genres'] = movies_df['genres'].apply(lambda x: (' ').join(x.split("|")))
	movies_df['intrating'] = movies_df['rating'].apply(lambda x: int(x))
	movies = movies_df[['title','genres','rating','intrating']].values.tolist()

	for index,[movie_title,genres,rating,intrating] in enumerate(movies):
		 # if index < 5:
		 # 	add_movie(index,movie_title,genres,rating,intrating,ia)
		 # else:
		 # 	break
		add_movie(index,movie_title,genres,rating,intrating,ia)

def add_movie(index,movie_title,genres,rating,intrating,ia):
	IMAGE_WIDTH = 182
	IMAGE_HEIGHT = 268
	try:
		movie = ia.search_movie(movie_title)[0]
		sr_title = movie['title'][:25]
		ln_title = movie['long imdb title']
		title = movie['title']
		yr = str(movie['year'])

		half_rating = True if rating > intrating else False

		movie_obj = Movie(title = title,short_title=sr_title,long_title=ln_title,year = yr,ratings=intrating,half_rating=half_rating,top_movie=False,genres=genres)
		img_field = movie_obj.image
		print(str(index)+" : "+movie['title'])

		resp = requests.get(movie['full-size cover url'])
		pillow_image = Image.open(BytesIO(resp.content))
		img_name= str(movie['title']) + ".jpg"

		img = resize_image(pillow_image,width=IMAGE_WIDTH,
	                  height=IMAGE_HEIGHT)

		img_field.save(img_name, InMemoryUploadedFile(img,None,img_name,'image/jpeg',img.tell,None))
		movie_obj.save()
	except IndexError as ie_error:
		print("Index Error: "+str(ie_error)+" : "+movie_title)
	except:
		print("Exception occured in movie: "+movie_title)

def resize_image(img, width, height):
	if img.size[0] > width or img.size[1] > height:
		new_image = img.resize((width,height))

	buffer = BytesIO()
	new_image.save(fp=buffer,format='JPEG')
	return ContentFile(buffer.getvalue())
