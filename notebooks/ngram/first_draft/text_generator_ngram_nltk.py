import numpy as np
import nltk

nltk.download('gutenberg')
from collections import defaultdict


# list of shakespeare corpora
shakespeare_corpora = [
    "shakespeare-caesar.txt",
    "shakespeare-hamlet.txt",
    "shakespeare-macbeth.txt"
]

# get all corpora
corpora = {
    corpus_name: nltk.corpus.gutenberg.words(corpus_name) for corpus_name in shakespeare_corpora
}

some_n_tokens = corpora["shakespeare-caesar.txt"][1002:1050]
print(" ".join(some_n_tokens))


# count how many times a specific token is right after another specific token
# in the corpora

# example: from the text "the dog is under the table.", we want to obtain the dictionary
# {
#  "the": { "dog": 1, "table": 1 },
#  "dog": { "is": 1 },
#  "is": { "under": 1 },
#  "under": { "the": 1 },
#  "table": { ".": 1 }
# }

# from_token_to_next_token_counts = { token: { next_token: num_of_occurrencies } }
from_token_to_next_token_counts = defaultdict(dict)

for corpus in corpora.values():
  for i in range(len(corpus) - 1):
    token = corpus[i].lower()
    next_token = corpus[i + 1].lower()
    if next_token not in from_token_to_next_token_counts[token]:
      from_token_to_next_token_counts[token][next_token] = 0
    from_token_to_next_token_counts[token][next_token] += 1

# print 10 examples of tokens that followed the token "from" in the corpora, along
# with their counts of occurrences
print(list(from_token_to_next_token_counts["mark"].items())[:10])


# transform occurrencies into probabilities

# example: from the text "the dog is under the table.", we want to obtain the dictionary
# {
#  "the": { "dog": 0.5, "table": 0.5 },
#  "dog": { "is": 1 },
#  "is": { "under": 1 },
#  "under": { "the": 1 },
#  "table": { ".": 1 }
# }

# from_token_to_next_token_probs = { token: { next_token: probability } }
from_token_to_next_token_probs = {}

for token, d_token in from_token_to_next_token_counts.items():
  sum_of_counts_for_token = sum(d_token.values())
  from_token_to_next_token_probs[token] = {
      next_token: count / sum_of_counts_for_token
      for next_token, count
      in d_token.items()
  }

# print 10 examples of tokens that followed the token "from" in the corpora, along
# with their probabilities
print(list(from_token_to_next_token_probs["rome"].items())[:10])


# sample the next token according to the computed probabilities
def sample_next_token(token, from_token_to_next_token_probs):
  next_tokens, next_tokens_probs = list(zip(*from_token_to_next_token_probs[token].items()))
  next_token_sampled = np.random.choice(next_tokens, size=1, p=next_tokens_probs)[0]
  return next_token_sampled

print(sample_next_token("rome", from_token_to_next_token_probs))


# repeatedly sample tokens to generate long text
def generate_text_from_token(token, from_token_to_next_token_probs, n_words_to_generate):
  text = token
  for _ in range(n_words_to_generate):
    next_token = sample_next_token(token, from_token_to_next_token_probs)
    text += " " + next_token
    token = next_token
  return text

first_token = "rome"
n_words_to_generate = 50
generated_text = generate_text_from_token(first_token, from_token_to_next_token_probs, n_words_to_generate)
print(generated_text)