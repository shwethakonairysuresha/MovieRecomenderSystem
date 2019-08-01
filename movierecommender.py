# import pandas library
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

m1 = 0
m2 = 0

# Get the data
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('file.tsv', sep='\t', names=column_names)
# Check the head of the data
print('file.tsv data:')
print(df.head())
print()

# Check out all the movies and their respective IDs
movie_titles = pd.read_csv('Movie_Id_Titles.csv')
print('Movie_Id_Titles data:')
print(movie_titles.head())
print()

#merge the two tables
data = pd.merge(df, movie_titles, on='item_id')
print('Merged table:')
print(data.head())
print()

#Here we do some exploratory data analysis to find some basic information on the data set
# Calculate mean rating of all movies
print('Mean rating of all movies:')
print(data.groupby('title')['rating'].mean().sort_values(ascending=False).head())
print()

# Calculate count rating of all movies
print(data.groupby('title')['rating'].count().sort_values(ascending=False).head())
print()

# creating dataframe with 'rating' count values
ratings = pd.DataFrame(data.groupby('title')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count())
print('Dataframe with rating count values:')
print(ratings.head())
print()

# plot graph of 'num of ratings column'
plt.figure(figsize=(10, 4))
ratings['num of ratings'].hist(bins=70)

# plot graph of 'ratings' column
plt.figure(figsize=(10, 4))
ratings['rating'].hist(bins=70)

#Create a matrix that has the user ids on one axis and the movie title on the other axis. Each cell consists of the
# rating the user gave to that movie. There will be a lot of Nan values bcoz most people would not have seen most movies.
# Sorting values according to the 'num of rating column'
moviemat = data.pivot_table(index='user_id',
                            columns='title', values='rating')
print('Matrix with user id on one axis and movies title on the other axis:')
print(moviemat.head())
# most rated movie
print(ratings.sort_values('num of ratings', ascending=False).head(10))
print()

#Calculating corelation
m1 = m1.mean()
m2 = m2.mean()
corrwith = np.sum(m1 - m2 / np.sqrt(np.sum(m1**2)*np.sum(m2**2)))

# analysing correlation with similar movies
starwars_user_ratings = moviemat['Star Wars (1977)']
liarliar_user_ratings = moviemat['Liar Liar (1997)']
print(starwars_user_ratings.head())
print()

# analysing correlation with similar movies
similar_to_starwars = moviemat.corrwith(starwars_user_ratings)
similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings)
corr_starwars = pd.DataFrame(similar_to_starwars, columns=['Correlation'])
corr_starwars.dropna(inplace=True)
print(corr_starwars.head())
print()

# Similar movies like starwars
print('Movies recommended that are similiar to star wars is:')
corr_starwars.sort_values('Correlation', ascending=False).head(10)
corr_starwars = corr_starwars.join(ratings['num of ratings'])
corr_starwars.head()
print(corr_starwars[corr_starwars['num of ratings'] > 100].sort_values('Correlation', ascending=False).head())
print()

# Similar movies as of liarliar
corr_liarliar = pd.DataFrame(similar_to_liarliar, columns=['Correlation'])
corr_liarliar.dropna(inplace=True)
corr_liarliar = corr_liarliar.join(ratings['num of ratings'])
print(corr_liarliar[corr_liarliar['num of ratings'] > 100].sort_values('Correlation', ascending=False).head())