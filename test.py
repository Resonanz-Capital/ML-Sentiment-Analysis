import nltk
import wordninja

from utils import get_df

# nltk.download('words')
# nltk.download('punkt')

# Example text
df = get_df(fund_id=3)
text = """
This is a sampletext that includes some mergedwordsfor example. These kinds of mistakes can often be found in OCR textdata, where spacemissingerrors are common.
"""

# Tokenize the text
tokens = nltk.word_tokenize(text)
print("Tokens:", tokens)

# Simple list of common English words for demo purposes, consider using a comprehensive dictionary or nltk.corpus.words
common_words = set(nltk.corpus.words.words())

def is_suspect(word):
    # You might adjust the length threshold based on your specific needs
    return len(word) > 12 or word.lower() not in common_words

suspect_words = [word for word in tokens if is_suspect(word)]
print("Suspect words:", suspect_words)

def needs_splitting(word):
    split_words = wordninja.split(word)
    return len(split_words) > 1

words_needing_split = [word for word in suspect_words if needs_splitting(word)]
print("Words needing split:", words_needing_split)
print("Count of words needing split:", len(words_needing_split))
