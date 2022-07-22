import pandas as pd
import numpy as np
import re
import nltk
pd.set_option('display.max_columns', None)


df = pd.read_csv("IMDB_Top250Engmovies2_OMDB_Detailed.csv")
df.head()

len(df)

df['Plot'][0]

#Data Preprocessing
# convert lowercase and remove numbers, punctuations, spaces, etc.,
df['clean_plot'] = df['Plot'].str.lower()
df['clean_plot'] = df['clean_plot'].apply(lambda x: re.sub('[^a-zA-Z]', ' ', x))
df['clean_plot'] = df['clean_plot'].apply(lambda x: re.sub('\s+', ' ', x))
df['clean_plot']


# tokenize the sentence
df['clean_plot'] = df['clean_plot'].apply(lambda x: nltk.word_tokenize(x))
df['clean_plot']

# remove stopwords
stop_words = nltk.corpus.stopwords.words('english')
plot = []
for sentence in df['clean_plot']:
    temp = []
    for word in sentence:
        if word not in stop_words and len(word) >= 3:
            temp.append(word)
    plot.append(temp)
plot

df['clean_plot'] = plot

df['clean_plot']

df.head()

df['Genre'] = df['Genre'].apply(lambda x: x.split(','))
df['Actors'] = df['Actors'].apply(lambda x: x.split(',')[:4])
df['Director'] = df['Director'].apply(lambda x: x.split(','))

df['Actors'][0]

def clean(sentence):
    temp = []
    for word in sentence:
        temp.append(word.lower().replace(' ', ''))
    return temp
    
df['Genre'] = [clean(x) for x in df['Genre']]
df['Actors'] = [clean(x) for x in df['Actors']]
df['Director'] = [clean(x) for x in df['Director']]

df['Actors'][0]

# combining all the columns data
columns = ['clean_plot', 'Genre', 'Actors', 'Director']
l = []
for i in range(len(df)):
    words = ''
    for col in columns:
        words += ' '.join(df[col][i]) + ' '
    l.append(words)
l

df['clean_input'] = l
df = df[['Title', 'clean_input']]
df.head()

#Feature Extraction
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer #tfidf and countvectorizer it weights the words according to their apperence times
tfidf = TfidfVectorizer()
features = tfidf.fit_transform(df['clean_input'])

# create cosine similarity matrix
from sklearn.metrics.pairwise import cosine_similarity #to measure the similarity between 2 nonzero vectors
cosine_sim = cosine_similarity(features, features)
print(cosine_sim)

#Movie Recommendation
index = pd.Series(df['Title'])
index.head()

def recommend_movies(title):
    movies = []
    idx = index[index == title].index[0] #indexing and selecting data
    # print(idx)
    score = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    top10 = list(score.iloc[1:11].index)
    # print(top10)
    
    for i in top10:
        movies.append(df['Title'][i])
    return movies
    
recommend_movies('The Dark Knight Rises')

index[index == 'The Dark Knight Rises'].index[0]

pd.Series(cosine_sim[3]).sort_values(ascending=False)

recommend_movies('The Shawshank Redemption')

recommend_movies('The Avengers')

len(df)
