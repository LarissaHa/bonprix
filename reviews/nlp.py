import re
import nltk
from nltk.corpus import stopwords
from germalemma import GermaLemma
from nltk.tag.sequential import ClassifierBasedTagger
import german_tagger
import pickle

def comment_to_topic(comment):

    # load and define stuff
    lemmatizer = GermaLemma()
    lemmas = []
    remove = [line.rstrip('\n') for line in open('add-stopwords.txt', encoding="utf-8")]
    exclude_words = remove + stop
    stop = stopwords.words('german')
    exclude = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'}
    with open('nltk_german_classifier_data.pickle', 'rb') as f:
        tagger = pickle.load(f)

    # sentence splitting
    comment = nltk.sent_tokenize(comment) 

    lemmas = []

    for j in range(len(comment)):
        # tokenization
        comment[j] = nltk.word_tokenize(comment[j])
        
        # punctuation removal
        comment[j] = [token for token in comment[j] if token not in exclude and token.isalpha()]
        
        # POS taging
        comment[j] = tagger.tag(comment[j])

        # lemmatization
        for k in range(len(comment[j])):
            try:
                lemmas.append(lemmatizer.find_lemma(comment[j][k][0], comment[j][k][1]))
            except ValueError:
                pass
    
    # lower
    lemmas = [word.lower() for word in lemmas]

    # stopword removal
    topics = [word for word in lemmas if word not in exclude_words]

    # make topics html-safe
    topics_safe = [t.replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('ß', 'ss') for t in topics]

    return topics, topics_safe