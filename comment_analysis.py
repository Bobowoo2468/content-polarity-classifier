import pandas as pd
import spacy
import re
import string
import nltk
import os
from googletrans import Translator
from pysentimiento import create_analyzer

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = 'python'

emotion_analyzer = create_analyzer(task="emotion", lang="en")
sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
toxicity_analyzer = create_analyzer(task="hate_speech", lang="en")

nlp = spacy.load("en_core_web_sm")


class CommentParser:
    @staticmethod
    def clean_comment(comment):
        comment = comment.split()
        words_to_filter = nltk.corpus.stopwords.words("english")
        comment_filtered = [word for word in comment if not word in words_to_filter]
        cleaned_comment = nlp(' '.join(comment_filtered))
        return cleaned_comment

    @staticmethod
    def translate_comment(comment):
        translator = Translator()

        # if comment is empty, nothing to translate
        if len(comment) == 0:
            return ""

        translated_comment = translator.translate(comment)
        # if translated_comment.src != "en":
        #     print(
        #         f"{translated_comment.origin} ({translated_comment.src}) --> "
        #         f"{translated_comment.text} ({translated_comment.dest})")
        return translated_comment

    @staticmethod
    def comment_sentiment(comment):
        return sentiment_analyzer.predict(comment)

    @staticmethod
    def comment_toxicity(comment):
        output = toxicity_analyzer.predict(comment).output
        if len(output) > 0:
            return True
        else:
            return False

    @staticmethod
    def full_comment_toxicity(comment):
        return toxicity_analyzer.predict(comment)

    @staticmethod
    def get_parsed_and_translated_comments(input_file):
        df = pd.read_csv(input_file)
        comments = df["Text"]
        translated_comments = []
        parsed_comments = []

        for comment in comments:
            translated_comment = CommentParser.translate_comment(comment).text
            parsed_comment = CommentParser.clean_comment(translated_comment)
            if translated_comment is not None:
                translated_comments.append(translated_comment)
            if parsed_comment is not None:
                parsed_comments.append(parsed_comment)

        return translated_comments, parsed_comments


if __name__ == "__main__":
    translated_comments, parsed_comments = CommentParser.get_parsed_and_translated_comments("./data/comments.csv")
    num_comments = len(translated_comments)

    cumulative_hatefulness = 0.0
    cumulative_aggression = 0.0
    cumulative_targeted = 0.0

    cumulative_hateful_count = 0
    cumulative_emotion_count = 0

    cumulative_emotion_dict = {"anger": 0.0, "disgust": 0.0, "joy": 0.0, "sadness": 0.0, "fear": 0.0, "surprise": 0.0}

    for c in translated_comments:
        emotion = emotion_analyzer.predict(c)
        toxicity = toxicity_analyzer.predict(c)
        if emotion.output != "others":
            cumulative_emotion_dict[emotion.output] += 1
            cumulative_emotion_count += 1
        if len(toxicity.output) > 0:
            cumulative_hateful_count += 1
        cumulative_hatefulness += toxicity.probas["hateful"]
        cumulative_aggression += toxicity.probas["aggressive"]
        cumulative_targeted += toxicity.probas["targeted"]

    print(f"cumulative_emotion_count: {cumulative_emotion_count}")
    print(f"cumulative_hateful_count: {cumulative_hateful_count}")
    print(f"cumulative_hatefulness: {cumulative_hatefulness}")
    print(f"cumulative_aggression: {cumulative_aggression}")
    print(f"cumulative_targeted: {cumulative_targeted}")

    print(f"Percentage cumulative emotion: {cumulative_emotion_count / num_comments}")
    print(f"Percentage cumulative hatefulness: {cumulative_hateful_count / num_comments}")
    print(f"Average cumulative hatefulness: {cumulative_hatefulness / num_comments}")
    print(f"Average cumulative aggression: {cumulative_aggression / num_comments}")
    print(f"Average cumulative targetedness: {cumulative_targeted / num_comments}")

    cumulative_pos = 0
    cumulative_neu = 0
    cumulative_neg = 0

    for c in translated_comments:
        print(c)
        sentiment = sentiment_analyzer.predict(c)
        print(sentiment.output)
        if sentiment.output == "POS":
            cumulative_pos += 1
        elif sentiment.output == "NEU":
            cumulative_neu += 1
        elif sentiment.output == "NEG":
            cumulative_neg += 1

    print(f"Percentage Positive Sentiment: {cumulative_pos / num_comments}")
    print(f"Percentage Neutral Sentiment: {cumulative_neu / num_comments}")
    print(f"Percentage Negative Sentiment: {cumulative_neg / num_comments}")

    print("")
    print(f"Final Summary of Feature Extraction")
    print(f"Emotional Polarity: {cumulative_emotion_count / num_comments}")
    print(f"Sentiment Polarity: {(cumulative_pos + cumulative_neg) / num_comments}")
    print(
        f"Comment Aggression: {(cumulative_hatefulness + cumulative_aggression + cumulative_targeted) / num_comments}")
