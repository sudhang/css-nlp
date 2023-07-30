import random
import nltk
from nltk.corpus import reuters

# Load the Reuters corpus
nltk.download('reuters')
corpus = reuters.fileids()

# Preprocess the text (tokenization, lowercase, etc.)
preprocessed_text = [word.lower() for word in reuters.words()]

# Train the n-gram model (let's consider a bigram model, n=2)
n = 2
ngram_model = {}
for i in range(len(preprocessed_text) - n):
    ngram = tuple(preprocessed_text[i:i+n])
    next_word = preprocessed_text[i+n]
    if ngram not in ngram_model:
        ngram_model[ngram] = []
    ngram_model[ngram].append(next_word)

# Generate fake news article
seed = ["breaking", "news:"]
max_length = 200
fake_article = seed

for _ in range(max_length):
    context = tuple(fake_article[-n+1:])
    if context not in ngram_model:
        break
    next_word = random.choice(ngram_model[context])
    fake_article.append(next_word)

# Print the generated fake news article
print(" ".join(fake_article))
