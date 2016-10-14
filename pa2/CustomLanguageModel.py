import math, collections

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.total = 0
    self.unigram = collections.defaultdict(int)
    self.bigram = collections.defaultdict(int)
    self.kn = collections.defaultdict(set)
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      context = None
      for datum in sentence.data: # iterate over datums in the sentence
        word = datum.word # get the word
        self.total += 1
        self.unigram[word] += 1
        self.bigram[(context, word)] += 1
        self.kn[word].add(context)
        context = word

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.
    context = sentence[0]
    for token in sentence[1:]: # iterate over words in the sentence
      #probability = self.absolute_discount(token, context)
      probability = self.kneser_ney(token, context)
      score += math.log(probability)
      context = token

    return score

  def absolute_discount(self, token, context):
    discount = 0.1
    add = 1.
    if self.unigram[context] > 0:
      bigram = max(self.bigram[(context, token)] - discount, 0.) / self.unigram[context]
      unigram = (self.unigram[token] + add) / (self.total + len(self.unigram) * add)
      lamb = discount * len(self.unigram) / self.unigram[context]
      return bigram + lamb * unigram
    else:
      unigram = (self.unigram[token] + add) / (self.total + len(self.unigram) * add)
      return unigram

  def kneser_ney(self, token, context):
    discount = 0.9
    add = 1.
    if self.unigram[context] > 0:
      bigram = max(self.bigram[(context, token)] - discount, 0.) / self.unigram[context]
      unigram =  (len(self.kn[token]) + add) / (len(self.bigram) + len(self.kn) * add)
      lamb = discount / self.unigram[context] * (len(self.kn[token]) + add)
      return bigram + lamb * unigram
    else:
      unigram =  (len(self.kn[token]) + add) / (len(self.bigram) + len(self.kn) * add)
      return unigram

