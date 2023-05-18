import nltk
import random
from nltk.util import ngrams
from collections import defaultdict

class ArticleGenerator:

    def __init__(self, n, filename):
        self.n = n
        self.model = self.build_model(filename)

    def build_model(self, filename):
        data = open(filename, 'r').read()
        token = nltk.word_tokenize(data)
        ngrams_list = list(ngrams(token, self.n))

        model = defaultdict(list)

        for gram in ngrams_list:
            model[gram[:-1]].append(gram[-1])

        return model

    def generate_sentence(self, seed=None, max_sentence_length=20):
        if seed is None:
            seed = random.choice(list(self.model.keys()))
        elif seed not in self.model:
            raise ValueError(f"The seed provided is not found in the model")

        sentence = list(seed)

        for _ in range(max_sentence_length):
            if tuple(sentence[-(self.n-1):]) in self.model:
                possible_words = self.model[tuple(sentence[-(self.n-1):])]
                next_word = random.choice(possible_words)
                sentence.append(next_word)
            else:
                break

        return ' '.join(sentence)

    def generate_article(self, num_sentences=10):
        article = []

        heading = self.generate_sentence(max_sentence_length=6)
        byline = f"By {self.generate_sentence(seed=('John',), max_sentence_length=2)}"
        location = f"{self.generate_sentence(seed=('New', 'York,'), max_sentence_length=2)} -"

        article.extend([heading, byline, location])

        for _ in range(num_sentences):
            sentence = self.generate_sentence()
            article.append(sentence)

        return "\n".join(article)


if __name__ == "__main__":
    n = 3  # specify n here
    filename = "data/bbc.txt"  # specify the filename here

    generator = ArticleGenerator(n, filename)
    print(generator.generate_article())
