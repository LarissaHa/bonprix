import re
import nltk
from nltk.corpus import stopwords
from germalemma import GermaLemma
import pickle

from nltk.tag.sequential import ClassifierBasedTagger

class ClassifierBasedGermanTagger(ClassifierBasedTagger):
    """A classifier based German part-of-speech tagger. It has an accuracy of
    96.09% after being trained on 90% of the German TIGER corpus. The tagger
    extends the NLTK ClassifierBasedTagger and implements a slightly modified
    feature detector.
    """

    def feature_detector(self, tokens, index, history):
        """Implementing a slightly modified feature detector.
        @param tokens: The tokens from the sentence to tag.
        @param index: The current token index to tag.
        @param history: The previous tagged tokens.
        """

        word = tokens[index]
        if index == 0: # At the beginning of the sentence
            prevword = prevprevword = None
            prevtag = prevprevtag = None
            #word = word.lower() # Lowercase at the beginning of sentence
        elif index == 1:
            prevword = tokens[index-1] # Note: no lowercase
            prevprevword = None
            prevtag = history[index-1]
            prevprevtag = None
        else:
            prevword = tokens[index-1]
            prevprevword = tokens[index-2]
            prevtag = history[index-1]
            prevprevtag = history[index-2]

        if re.match('[0-9]+([\.,][0-9]*)?|[0-9]*[\.,][0-9]+$', word):
            # Included "," as decimal point
            shape = 'number'
        elif re.compile('\W+$', re.UNICODE).match(word):
            # Included unicode flag
            shape = 'punct'
        elif re.match('([A-ZÄÖÜ]+[a-zäöüß]*-?)+$', word):
            # Included dash for dashed words and umlauts
            shape = 'upcase'
        elif re.match('[a-zäöüß]+', word):
            # Included umlauts
            shape = 'downcase'
        elif re.compile("\w+", re.UNICODE).match(word):
            # Included unicode flag
            shape = 'mixedcase'
        else:
            shape = 'other'

        features = {
            'prevtag': prevtag,
            'prevprevtag': prevprevtag,
            'word': word,
            'word.lower': word.lower(),
            'suffix3': word.lower()[-3:],
            #'suffix2': word.lower()[-2:],
            #'suffix1': word.lower()[-1:],
            'preffix1': word[:1], # included
            'prevprevword': prevprevword,
            'prevword': prevword,
            'prevtag+word': '%s+%s' % (prevtag, word),
            'prevprevtag+word': '%s+%s' % (prevprevtag, word),
            'prevword+word': '%s+%s' % (prevword, word),
            'shape': shape
            }
        return features

def comment_to_topic(comment):

    # load and define stuff
    lemmatizer = GermaLemma()
    lemmas = []
    remove = [line.rstrip('\n') for line in open('reviews/add-stopwords.txt', encoding="utf-8")]
    stop = stopwords.words('german')
    exclude_words = remove + stop
    exclude = {'!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'}
    
    
    with open('reviews/nltk_german_classifier_data.pickle', 'rb') as f:
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
