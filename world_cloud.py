"""



Author: @AnitaSrbinovska
"""

# This program generates a word cloud from word frequency data in a CSV file and saves it as a PNG image.

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random

# Load data as pandas dataframe
df = pd.read_csv('tokens_uof.csv')

# Strip any leading or trailing whitespace from the column names
df.columns = [col.strip() for col in df.columns]

# 'word' column is a string column
df['word'] = df['word'].astype(str)

# Create a dictionary from the dataframe
data = {row['word']: row['count'] for _, row in df.iterrows()}

# Generate word cloud from frequencies with larger size
wc = WordCloud(background_color="white", width=1600, height=800, max_words=1000).generate_from_frequencies(data)

# Define the average count for color function
average_count = df['count'].mean()

# Color function to color words based on their frequency with random colors
def random_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "rgb({}, {}, {})".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Apply random color function to word cloud
wc.recolor(color_func=random_color_func)

# Save final result as a PNG file
plt.figure(figsize=(20, 10))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.savefig('word_cloud_uof.png', format='png')
plt.close()
