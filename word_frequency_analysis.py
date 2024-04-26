import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
import urllib.request
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
from cleantext import clean
import pandas as pd

nltk.download("stopwords")
nltk.download('punkt')

if __name__ == "__main__":
    df = pd.read_csv("./data/transcript.csv")
    transcript_texts = df["Text"]
    text = " ".join(transcript_texts)

    words = word_tokenize(text)
    words_no_punc = []
    clean_words = []
    stopwords_list = stopwords.words("english")
    stopwords_list_no_punc = [clean(word, no_punct=True) for word in stopwords_list]
    stopwords_list_no_punc.extend(["im", "like", "thats", "number", "lets", "theres"])

    print(f"Total number of words in text is: {len(words)}")

    freq_dist = FreqDist(words)
    print("Top 10 most common words", freq_dist.most_common(10))

    for word in words:
        if word not in stopwords_list_no_punc:
            if word.isalpha():
                clean_words.append(word.lower())

    freq_dist = FreqDist(clean_words)
    print(f"The total number of words without punctuation and stopwords is {len(clean_words)}")
    print("Top 10 most common words after filtering", freq_dist.most_common(10))

    # Plot the 10 most common words
    freq_dist.plot(10)
    plt.show()

    # Convert word list to a single string
    clean_words_string = " ".join(clean_words)

    # generating the wordcloud
    wordcloud = WordCloud(background_color="white").generate(clean_words_string)

    # plot the wordcloud
    plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud)

    # to remove the axis value
    plt.axis("off")
    plt.show()
