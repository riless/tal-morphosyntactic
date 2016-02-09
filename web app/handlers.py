# -*- coding: utf-8 -*-
import os
import pickle as pk
import time
import tornado.web
import numpy as np
import sys

from nltk.tag.stanford import POSTagger
from nltk.corpus import PlaintextCorpusReader
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer
import matplotlib.pyplot as plt

os.environ['JAVAHOME'] = '/usr/lib/jvm/java-8-oracle/bin'
os.environ['STANFORD_PARSER'] = '/opt/stanford-parser'
os.environ['STANFORD_MODELS'] = '/opt/stanford-parser'

french_model = "/opt/stanford-postagger/models/french.tagger"
stanford_tagger_jar = "/opt/stanford-postagger/stanford-postagger.jar"
tagger = POSTagger(french_model, stanford_tagger_jar, encoding="utf-8")

corpus_file = r"xaa"
corpus_path = "fr-en/"

test_corpus_file = r"xae"
test_corpus_path = "fr-en/"

dict_file = "dict_tree.pk"

errors = {1:"small-error", 2: "medium-error", 3:"big-error"}
def render(sentence, ruptures):
    output = u""
    for i, word in enumerate(sentence):
        if (ruptures[i]>=1 and ruptures[i] <= 3):
            output += '''<span class="%s">%s </span>'''% (errors[ruptures[i]], word)
        else:
            output += word + " "
    return output.encode('utf8')

tree = {}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class Analyzer(tornado.web.RequestHandler):
    def initialize(self):
        if os.path.exists( dict_file ):
            print "loading model..."
            self.model = pk.load( open(dict_file, "rb") )
            print len(self.model)
            # self.total = len(self.model)
            # y = []
            # for c,v in model:
            #     y.append(v)
            # plt.scatter(np.arrange(len(y)), y, s=area, c=colors, alpha=0.5)
            # plt.show()
        else:
            sys.exit( "model not found !" )
    
    def post(self):
        text = self.get_argument("i").strip()
        print text


        # for m in model.items():
        #     self.write( str(m) )

        # y = []
        # for k, v in model.items():
        #     y.append(v)
        # x = range(len(y))
        # plt.plot(x, y)
        # plt.ylim( [0,5000] )
        # plt.show()

        # reader = PlaintextCorpusReader(test_corpus_path, test_corpus_file)
        # sentences = reader.sents()
        
        # data = u"je suis suis chat"
        sentences = WhitespaceTokenizer().tokenize(text)
        sentences_tags = tagger.tag_sents( [sentences] )
        # print "data: ", data
        # print "sentences: ", sentences
        # print "sentences_tags: ", sentences_tags

        ok = 0
        notok = 0

        for sentence_tags in sentences_tags:
            tags = [ tag for (word, tag) in sentence_tags ]

            nb_words = len( tags )
            ruptures = np.zeros(nb_words, dtype=np.int8)
            if ( nb_words < 3 ):
                self.write("<i>Votre phrase doit contenir aux moins 3 mots pour pouvoir être analysée</i>")
            else:
                # ruptures[-2:] = [0] * 2

                trigrams=ngrams(tags,3)
                for i, b in enumerate(trigrams):
                    print "bi: ", b
                    if self.model.has_key(b) and self.model[b] > 1000:
                        print str(b)+"\t\t"+str(self.model[b])+"\t\tok<br>"
                        ok += 1
                    else:
                        ruptures[i:i+3] += 1
                        print str(b)+"\t\tnot ok<br>"
                        notok += 1
                # self.write( str(ruptures) )
                self.write( render(sentences, ruptures ) )


