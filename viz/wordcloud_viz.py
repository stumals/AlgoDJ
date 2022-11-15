import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
from pathlib import Path


# Pull in the data
sample_size = 30
df = pd.read_csv(Path("data", "music_data_1k.csv"))
df1 = df.sample(sample_size)

newlist = []
for i in range(0, len(df1)):
    s = df1.iloc[i]["artists"]
    result = re.search("\['(.*)'\]", s).group(1)
    firstartist = result.split(",")[0].replace("'", "")
    newlist.append(firstartist)

frequencies = [1 for _ in range(len(df1))]

d = dict(zip(newlist, frequencies))
wordcloud = WordCloud(collocations=False).generate_from_frequencies(d)
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(Path("viz", "artist_wordcloud.png"), bbox_inches="tight")
