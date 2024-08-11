import nltk
import random
from nltk.util import ngrams
from collections import defaultdict


nltk.download('punkt')

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
        if seed is not None and seed in self.model:
            sentence = list(seed)
        else:
            sentence = list(random.choice(list(self.model.keys())))

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
        byline = f"By {self.generate_sentence(seed=('Ukraine', 'with'), max_sentence_length=2)}"
        location = f"{self.generate_sentence(seed=('The', 'UK'), max_sentence_length=2)} -"

        article.extend([heading, byline, location])

        for _ in range(num_sentences):
            sentence = self.generate_sentence()
            article.append(sentence)

        return "\n".join(article)


if __name__ == "__main__":
    n = 5  # specify n here
    filename = "data/bbc.txt"  # specify the filename here

    generator = ArticleGenerator(n, filename)
    print(generator.generate_article())
