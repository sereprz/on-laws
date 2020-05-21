import spacy
from pyphen import Pyphen


class Scorer:

    nlp = spacy.load('en')

    def __init__(self, lang='en_US'):
        
        self.dic = dic = Pyphen(lang=lang)

    def syllables(self, w):
        '''
            Return the list of syllables in w
            :param w: str, a word
        '''
        return self.dic.inserted(w).split('-')
        
    def syllable_count(self, w):
        '''
            Return the number of syllables in w
            :param w: str, a word
        '''
        return len(self.syllables(w))
    
    def WPS(self, doc):
        '''
            Average number of words per sentence
            :param doc: spacy.tokens.doc.Doc
        '''
        n_words = len([t for t in doc if t.is_alpha])
        n_sentences = len(list(doc.sents))
        try:
            return n_words / n_sentences
        except ZeroDivisionError:
            return 200

    def SPW(self, doc):
        '''
            Average number of syllables per word
            :param doc: spacy.tokens.doc.Doc
        '''
        n_words = len([t for t in doc if t.is_alpha])
        n_syllables = sum([self.syllable_count(t.text) for t in doc if t.is_alpha])
        try:
            return n_syllables / n_words
        except ZeroDivisionError:
            return 200
    
    def FleschScore(self, text):
        '''
            Computes the Flesch reading-ease test, higher scores indicatematerial that is easier to read; lower numbers mark passagesthat are more difficult to read.
            :param text: str
        '''
        doc = self.nlp(text)
        return round(206.835 - 1.015 * self.WPS(doc) - 84.6 * self.SPW(doc))
