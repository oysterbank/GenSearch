# GenSearch v0.1
# Evolutionary Document Search using genetic algorithms
# 
# Authors: Kris Laratta, Aman Mundra, and Priyank Srivastava

from __future__ import division
import nltk
from nltk.corpus import PlaintextCorpusReader
corpus_root = './CorpusDocs'
wordlists = PlaintextCorpusReader(corpus_root,'.*')

print"\n\n---- TEST RUN"
print "\nAll the files in the corpus", wordlists.fileids()
print "\n"

def Initial_search(search_input):
	
	"""Looking for the Docs in the Pool"""
	file_list = wordlists.fileids()
	matrix = []
	for f2 in file_list:
		words_in_files = wordlists.words(f2)
		fd = nltk.FreqDist(w.lower() for w in words_in_files)
		matrix.append((f2,fd[search_input]))

	sortd = sorted(matrix, key=lambda tup: tup[1])

	"""Brings top Documents"""
	Top_DOC = sortd[::-1]

	"""Bring most common words"""	
	top_words = []
	for i in range(0,4):
		file_name = Top_DOC[i][0]
		words_in_files = wordlists.words(file_name)
		for w in words_in_files:
			top_words.append(w)
	fd2 = nltk.FreqDist(w.lower() for w in top_words)
	test = fd2.most_common(5)
	testset = [x[0] for x in test]
	print "\nMost Common words with search term", search_input
	print [element for element in testset]
	
	"""Count of the most common words"""
	count = []
	for key in testset:
		count.append(fd2[key])
	print "There occurence in top 5 Documents",count

	total = sum(count)

	"""Fractional Weights of the most common words"""
	fd_weights = []
	for k in count:
		fr = k/total
		fd_weights.append(fr)

	return testset, fd_weights 

print "====================================================="
def CWFD_calc( testset,fd_weights ):
	print "\n"
	Fitness_score = []
	save_file = []
	List_of_files = wordlists.fileids()
	print ""
	for f1 in List_of_files:
		print "---------File Start ",f1, " ----------------------"
		words_in_files = wordlists.words(f1)
		freq_dist = nltk.FreqDist(w.lower() for w in words_in_files)
		count_in_file = []
		for key in testset:
			count_in_file.append(freq_dist[key])
		CWFD_prime = [a*b for a,b in zip(count_in_file,fd_weights)]
		print "\nCWFD---",CWFD_prime
		print "Fitness Score--", sum(CWFD_prime)
		Fitness_score.append(sum(CWFD_prime))
		save_file.append(f1)
		print "---------File end-------------------------------\n"

	return Fitness_score, save_file

print "\n====Our New Search tech====\n"
ask = 'n'
s = 0
while ask == 'y' or "Yes":
	s = s + 1
	search_input = str(raw_input("\nEnter the search term- ")).lower()
	x,y = Initial_search(search_input)
	CWFD_calc(x,y)

	if s==1:
		FD_weights_Search1 = [ a*0.25 for a in y ]
		Composite_1st = zip(x,FD_weights_Search1)
		testset_1st = x
	if s>1:
		FD_weights_Search2 = [ a*0.75 for a in y ]
		Composite_2nd = zip(x, FD_weights_Search2)
		testset_2nd = x

	print "\nDo you want to continue searching (Y/N)"
	ask = str(raw_input()).lower()
	if ask == 'n':
		break

if s>1:
	F1, save_f1 = CWFD_calc( testset_2nd, FD_weights_Search2 )
	F2, save_f2 = CWFD_calc( testset_1st, FD_weights_Search1 )
	Fit = [(a+b) for a,b in zip( F1, F2 )]
	Final = zip( save_f1, Fit)
	Final_sortd = sorted(Final, key=lambda tup: tup[1])
	Get_Doc = Final_sortd[::-1]
	for i in range(0,len(Get_Doc)):
		print Get_Doc[i]
	print "\n"
	print "============================ RESULT ==============================="
	print "DOCUMENT is", Get_Doc[0][0], "and FITNESS SCORE is ", Get_Doc[0][1]
	print ""
    