# GenSearch v0.8
# Evolutionary Document Search using genetic algorithms
# 
# Authors: Kris Laratta, Aman Mundra, and Priyank Srivastava

from __future__ import division
import nltk
from nltk.corpus import PlaintextCorpusReader
corpus_root = '/home/priyank/Desktop/AI/Project'
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
		#print f2, "---- count ---", fd[search_input]
		matrix.append((f2,fd[search_input]))
	#print matrix

	sortd = sorted(matrix, key=lambda tup: tup[1])
	#print "\n  ", "  ", sortd[::-1]

	"""Brings top Documents"""
	Top_DOC = sortd[::-1]
	#for i in range(0,4):
		#print Top_DOC[i]

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
	#print "\nTotal Sum--", total

	"""Fractional Weights of the most common words"""
	fd_weights = []
	for k in count:
		fr = k/total
		fd_weights.append(fr)
	#print "fd_weights",fd_weights

	return testset, fd_weights 

print "====================================================="
def CWFD_calc( testset,fd_weights ):
	#This function calculates all the 
	print "\n"
	Fitness_score = []
	save_file = []
	# for f1 in range(0,4):
	# 	my_file = Top_DOC[f1][0]
	# 	print "File-", my_file
	# 	words_in_files = wordlists.words(my_file)
	# 	print type(words_in_files)
	List_of_files = wordlists.fileids()
	#print "\n\nList_of_files", List_of_files
	print ""
	for f1 in List_of_files:
		# f1 pulls all the file names.
		print "---------File Start ",f1, " ----------------------"
		words_in_files = wordlists.words(f1)
		freq_dist = nltk.FreqDist(w.lower() for w in words_in_files)
		count_in_file = []
		for key in testset:
			count_in_file.append(freq_dist[key])
		#print "count_in_file", count_in_file
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
save_fd_weights = []
save_mostcommon = []
Fit = []
save_file_final = []
while ask == 'y' or "Yes":
	s = s + 1
	print s
	search_input = str(raw_input("\nEnter the search term- ")).lower()
	x,y = Initial_search(search_input)  # 1st function call	
	save_fd_weights.append(y)
	save_mostcommon.append(x)
	
	fit_1st, files_1st = CWFD_calc(x,y)
	
	Final = zip( files_1st, fit_1st )
	Final_sortd = sorted(Final, key=lambda tup: tup[1])
	Get_Doc = Final_sortd[::-1]
	for i in range(0,len(Get_Doc)):
		print Get_Doc[i]
	print "\n"
	print "============================ RESULT ==============================="
	print "DOCUMENT is", Get_Doc[0][0], "and FITNESS SCORE is ", Get_Doc[0][1]
	print ""

	if s>1:
		""" The last search of the user """
		last_search = save_fd_weights[-1]
		FD_weight_final = [a*0.75 for a in last_search] 
		wt=0.25/(s-1)
		
		print last_search
		print FD_weight_final
		print wt
		
		Final_fitness, save_file_final = CWFD_calc(x,FD_weight_final)
		F = Final_fitness
		
		""" Loop for intermediate searches """
		fd_intermediate = []
		save_f1 = []
		
		loop_length=len(save_fd_weights) - 1  
		
		for x in range(0,loop_length):
			fd_intermediate = [a*wt for a in save_fd_weights[x]]
			F1, save_f1 = CWFD_calc(save_mostcommon[x], fd_intermediate)
			Fit = [(a+b) for a,b in zip( F1, F)]
			F = Fit
			

		Final_zip = zip( save_file_final, Fit )
		Final_sort = sorted(Final_zip, key=lambda tup: tup[1])
		Get_Doc_final = Final_sort[::-1]
		for i in range(0,len(Get_Doc_final)):
			print Get_Doc_final[i]
		print "\n"
		print "============================ RESULT ==============================="
		print "DOCUMENT is", Get_Doc_final[0][0], "and FITNESS SCORE is ", Get_Doc_final[0][1]
		print ""

	# x is testset -- most common words
	# y is fd_weights 
	# if s==1:
	# 	FD_weights_Search1 = [ a*0.25 for a in y ]
	# 	Composite_1st = zip(x,FD_weights_Search1)
	# 	testset_1st = x
	# 	#print "\n FD_weights_Search1", Composite_1st
	# if s>1:
	# 	FD_weights_Search2 = [ a*0.75 for a in y ]
	# 	Composite_2nd = zip(x, FD_weights_Search2)
	# 	testset_2nd = x
		#print "\n FD_weights_Search2", zip(x, FD_weights_Search2) 
	
	print "\nDo you want to continue searching (Y/N)"
	ask = str(raw_input()).lower()
	if ask == 'n':
		break
# if s>1:
# 	#print "\n\n===== Composite Stuff ====="
# 	F1, save_f1 = CWFD_calc( testset_2nd, FD_weights_Search2 )
# 	F2, save_f2 = CWFD_calc( testset_1st, FD_weights_Search1 )
# 	Fit = [(a+b) for a,b in zip( F1, F2 )]
# 	#print "Final Fitness score ", Fit
# 	Final = zip( save_f1, Fit)
# 	Final_sortd = sorted(Final, key=lambda tup: tup[1])
# 	Get_Doc = Final_sortd[::-1]
# 	for i in range(0,len(Get_Doc)):
# 		print Get_Doc[i]
# 	print "\n"
# 	print "============================ RESULT ==============================="
# 	print "DOCUMENT is", Get_Doc[0][0], "and FITNESS SCORE is ", Get_Doc[0][1]
# 	print ""
#=================================End of the program========================