import math, collections

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.unigram = collections.defaultdict(int)
    self.bigram = collections.defaultdict(int)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      context = None
      for datum in sentence.data: # iterate over datums in the sentence
        word = datum.word # get the word
        self.unigram[word] += 1
        self.bigram[(context, word)] += 1
        context = word

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.
    context = None
    for token in sentence: # iterate over words in the sentence
      probability = (self.bigram[(context, token)] + 1.) / (self.unigram[context] + len(self.unigram))
      score += math.log(probability)
      context = token

    return score

