import nltk
# nltk.download('sentiwordnet')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

from comment_analysis import CommentParser


class LexicalAnalysis:

    @staticmethod
    def penn_to_wn(tag):
        """
        Convert between the PennTreebank tags to simple Wordnet tags
        """
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        return None

    @staticmethod
    def tokenise_and_tag(comments):
        token_tag_pairs = []

        for sentence in comments:
            token = nltk.word_tokenize(sentence)
            after_tagging = nltk.pos_tag(token)
            for pair in after_tagging:
                token_tag_pairs.append(pair)

        return token_tag_pairs

    @staticmethod
    def cumulative_sentiment_subjectivity(token_tag_pairs):
        sentiment = 0.0
        objectivity = 0.0
        tokens_count = 0

        lemmatizer = WordNetLemmatizer()
        for word, tag in token_tag_pairs:
            wn_tag = LexicalAnalysis.penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue

            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue

            # Take the first sense, the most common
            synset = synsets[0]
            swn_synset = swn.senti_synset(synset.name())
            print(swn_synset)

            sentiment += swn_synset.pos_score() - swn_synset.neg_score()
            objectivity += swn_synset.obj_score()
            tokens_count += 1

        print(f"Total tokens classified: {tokens_count}")
        print(f"Total sentiment: {sentiment}")
        print(f"Total objectivity: {objectivity}")
        print(f"Cumulative sentiment: {sentiment / tokens_count}")
        print(f"Cumulative objectivity: {objectivity / tokens_count}")

        print("")
        print(f"Final Summary of Feature Extraction")
        print(f"Transcript Objectivity: {objectivity / tokens_count}")


if __name__ == "__main__":
    translated_comments, parsed_comments = CommentParser.get_parsed_and_translated_comments("./data/transcript.csv")

    token_tag_pairs = LexicalAnalysis.tokenise_and_tag(translated_comments)
    LexicalAnalysis.cumulative_sentiment_subjectivity(token_tag_pairs)
