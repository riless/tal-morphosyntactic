# -*- coding: utf-8 -*-
import sys
import os
import pickle as pk
import time
import matplotlib.pyplot as plt
import numpy as np

from nltk.tag.stanford import POSTagger
from nltk.corpus import PlaintextCorpusReader
from nltk.util import ngrams
from nltk.tokenize import WhitespaceTokenizer

# import nltk
# from nltk.corpus import inaugural
# from nltk.tokenize import word_tokenize
# from nltk.tag import map_tag
# import nltk.data

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

def render(sentence, ruptures):
	print len( sentences )
	print len( ruptures )
	output = ""
	for i, word in enumerate(sentence):
		rup = " | " if ruptures[i] == 1 else " "
		output += word + rup
	return output.encode('utf8')
# text = """
# Je déclare reprise la session du Parlement européen qui avait été interrompue le vendredi 17 décembre dernier et je vous renouvelle tous mes vux en espérant que vous avez passé de bonnes vacances.
# Vous avez souhaité un débat à ce sujet dans les prochains jours, au cours de cette période de session.
# """
# sentences = WhitespaceTokenizer().tokenize(text)
# sentences_tags = tagger.tag_sents( [sentences] )
tree = {}
if os.path.exists( dict_file ):
	print "loading model..."
	model = pk.load( open(dict_file, "rb") )
	print len(model)
	# y = []
	# s = 0
	# for c,v in model.items():
	#     y.append(v)
	#     s += v
	# print "s=", s 
	plt.scatter(np.arange(len(y)), y, alpha=0.5)
	plt.ylim((0,100))
	plt.show()

	sys.exit()

	reader = PlaintextCorpusReader(test_corpus_path, test_corpus_file)
	sentences = reader.sents()
	
	# data = u"je suis suis chat"
	# sentences = WhitespaceTokenizer().tokenize(data)

	sentences_tags = tagger.tag_sents( sentences )
	ok = 0
	notok = 0

	for sentence_tags in sentences_tags:
		tags = [ tag for (word, tag) in sentence_tags ]

		nb_words = len( tags )
		ruptures = [1] * ( nb_words )

		trigrams=ngrams(tags,3)
		for i, b in enumerate(trigrams):
			if model.has_key(b) and model[b] > 100:
				ruptures[i:i+3] = [0] * 3
				# print b, "\t\t",model[b],"\t\tok"
				ok += 1
			else:
				# print b, "\t\tnot ok"
				notok += 1
	print "ok = ", ok
	print "not ok = ", notok
	print "ratio = ", ( ok // (ok + notok) ) * 100, "de bonne classif"
		# print render(sentences, ruptures)


	'''
		for t,occ in model:
			print t,"\t\t",occ
	'''

else:
	print "creating model..."
	# sentences = inaugural.sents(corpus)
	reader = PlaintextCorpusReader(corpus_path, corpus_file)
	sentences = reader.sents()
	total = len( sentences )
	# sentences = [ u"Le chien est sur la table.", u"Le chat est sous le canapé"]
	i = 0
	avg_time = 0
	print time.clock(), "tagging..."
	sentences_tags = tagger.tag_sents( sentences )

	print time.clock(), "building tree..."
	for sentence_tags in sentences_tags:
		# print 
		# print sentence_tags
		# print 
		tags = [ tag for (word, tag) in sentence_tags ]
		bigrams=ngrams(tags,3)
		for b in bigrams:
			if b in tree:
				tree[b] += 1
			else:
				tree[b] = 1
	print "# Tree #"
	print tree

	print time.clock(), "saving tree..."
	with open( dict_file, "wb") as f:
		pk.dump( tree, f )
	print "Done!"
	'''
	for sentence in sentences:
		if i == 2:
			break; 
		i += 1
		print "\n",i, "/", total
		tic = time.clock()
		# print time.clock(), "tagging"

		pos_tuples = tagger.tag(sentence)
		# print time.clock(), "convert to tags"
		for pos_tuple in pos_tuples:
			tags = [ tag for (word, tag) in pos_tuple ]
		
		for t in pos_tuple:
			print t
		# token=nltk.word_tokenize(tags)
		# print time.clock(), "convert to trigrams"
		bigrams=ngrams(tags,3)
		# print time.clock(), "add to tree\n"
		for b in bigrams:
			if b in tree:
				tree[b] += 1
			else:
				tree[b] = 1
		tac = time.clock()
		avg_time = (avg_time + tac-tic) / 2 
		print "temps restant", avg_time * (total - i)
	print tree
	'''
	"""

	"""
	'''

	# GUI
	for line in sentences:
	    for sentence in line:
	        sentence.draw()
	'''
