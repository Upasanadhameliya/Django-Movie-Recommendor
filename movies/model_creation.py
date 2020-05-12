import pandas as pd
from moviedisp.models import Movie
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def create():
	movies = Movie.objects.all().filter(top_movie=False)
	genrelist = []

	for movie in movies:
		genrelist.append(movie.genres)

	genres = pd.Series(genrelist)
	print(genres.size)

	#genres = genres.apply(lambda x: x.split(" "))
	print(genres.head(n=20))

	vectorizer = TfidfVectorizer(analyzer="word",min_df=0,ngram_range=(1,2),stop_words="english")
	tfidf_matrix = vectorizer.fit_transform(genres)
	cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
	cosine_pd = pd.DataFrame(cosine_sim)

	with open("modelfile.sav","wb") as f:
		pickle.dump(cosine_sim,f)

	print(cosine_pd.head(n = 20))
