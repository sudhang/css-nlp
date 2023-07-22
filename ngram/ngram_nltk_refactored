

from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk
import os


# Function to tokenize text using NLTK tokenizer or fallback to a naive tokenizer
def tokenize_text(text):
    try:  # Use the default NLTK tokenizer.
        from nltk import word_tokenize, sent_tokenize
        return word_tokenize(sent_tokenize(text)[0])
    except:  # Use a naive sentence tokenizer and toktok.
        import re
        from nltk.tokenize import ToktokTokenizer
        sent_tokenize = lambda x: re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', x)
        toktok = ToktokTokenizer()
        return toktok.tokenize(text)


# Function to preprocess text for n-grams language modeling
def preprocess_corpus(corpus, n):
    processed_corpus = [tokenize_text(text) for text in corpus]
    train_data, padded_sents = padded_everygram_pipeline(n, processed_corpus)
    return train_data, padded_sents


# Function to train an n-gram language model
def train_ngram_model(train_data, padded_sents, n):
    model = MLE(n)
    model.fit(train_data, padded_sents)
    return model


# Function to generate a sentence using the trained n-gram model
def generate_sentence(model, num_words, random_seed=42):
    content = []
    for token in model.generate(num_words, random_seed=random_seed):
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
    return TreebankWordDetokenizer().detokenize(content)


# Main function to execute the code for processing multiple .txt files
def process_multiple_txt_files(txt_folder_path, n=3, num_words=20, random_seed=42):
    nltk.download('punkt')
    # List all .txt files in the specified folder
    txt_files = [f for f in os.listdir(txt_folder_path) if f.endswith('.txt')]

    # Preprocess and train the n-grams language model for each file
    all_sentences = []
    for txt_file in txt_files:
        txt_file_path = os.path.join(txt_folder_path, txt_file)
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            # Read the text from the .txt file
            text = file.read()


        # Preprocess the tokenized text for n-grams language modeling
        train_data, padded_sents = preprocess_corpus([text], n)

        # Train the n-grams language model
        model = train_ngram_model(train_data, padded_sents, n)

        # Generate a sentence using the trained model
        sentence = generate_sentence(model, num_words, random_seed)
        all_sentences.append(sentence)

    return all_sentences


if __name__ == "__main__":
    # Example usage for processing multiple .txt files in a folder
    txt_folder_path = 'ngram/data/txt_corpus'  # Modify this line with your folder path
    sentences = process_multiple_txt_files(txt_folder_path, n=3, num_words=50, random_seed=42)
    for i, sentence in enumerate(sentences):
        print(f"Sentence {i+1}: {sentence}")
