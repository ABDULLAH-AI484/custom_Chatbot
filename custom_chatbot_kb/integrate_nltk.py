import nltk
# # nltk.download("wordnet")
from nltk.corpus import wordnet as wn

def getDefinition(word):
    try:
        s = wn.synset(word + '.n.01')
        return s.definition()
    except Exception as e:
        return "Sorry, I couldn't find a definition for that word."