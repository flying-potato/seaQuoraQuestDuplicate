# clean stop word and stemming text, then pickled cleaned text to files
# data structure is

'''
PICKLE DATASTRUCTURE:
key : id 
value:
	dict:
	question1
	question2
	is_duplicate : 0 or 1
'''
# id - the id of a training set question pair
# qid1, qid2 - unique ids of each question (only available in train.csv)
# question1, question2 - the full text of each question
# is_duplicate - the target variable, set to 1 if question1 and question2 have essentially the same meaning, and 0 otherwise.

#  e.g. "11","23","24","How do I read and find my YouTube comments?","How can I see all my Youtube comments?","1"

from nltk.stem import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string, pickle , os, sys, json, csv
import argparse

stemmer1 = SnowballStemmer("english", ignore_stopwords=True)
split_return = lambda line_text, index: (line_text.split(","))[index]

def stem_cleaned_text (text):
	global stemmer1
	text = text.strip('"')
	stop_words = set(stopwords.words("english"))  # load stopwords
	wordsToken = word_tokenize(text) 
	wordsToken = filter(lambda x: x not in string.punctuation, wordsToken)
	cleaned_text = filter(lambda x: x not in stop_words, wordsToken)
	stemmed_words = map (lambda x: stemmer1.stem(x) , cleaned_text )
	return list(stemmed_words)

def stem_file(data_dir, data_filename):
	out_filename = data_filename + ".out"
	#read infile, and pickle to outfile
	ret_dict = {}
	data_path = os.path.join( data_dir, data_filename)
	out_path  =  os.path.join( data_dir, out_filename) 
	out_file = os.path.join( data_dir, data_filename + ".out"+'_f') 
	with open(out_path, 'wb')  as outfile:
		outfile_f = open(out_file, 'w')
		with  open(data_path, newline = '') as infile:
			infilereader = csv.reader(infile)
			next(infilereader, None)
			for line_text in infilereader:
				id = line_text[0]
				q1 = line_text[3]
				q2 = line_text[4]
				is_duplicate_bit = line_text[5]
				stemmed_q1 = stem_cleaned_text(q1)
				stemmed_q2 = stem_cleaned_text(q2)
				ret_dict[id] ={  'question1': stemmed_q1, 'question2':stemmed_q2, 'is_duplicate': is_duplicate_bit }
		pickle.dump(ret_dict, outfile)
		outfile_f.write( json.dumps(ret_dict, indent =2 ) )
		outfile_f.close()


def get_par_dir():
	print(__file__)
	parpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
	print("parent path is: " ,parpath)
	datapath = os.path.join(parpath, 'data')
	return (parpath, datapath)


if __name__ == "__main__":
	# text = "This is a sample sentence, showing off the stop words filtration filtr samples that."
	pardir, datadir = get_par_dir()
	parser = argparse.ArgumentParser(description='process different input.')
	parser.add_argument("-i",type=str, dest = "inputfile")
	args = parser.parse_args()
	

	stem_file(datadir ,args.inputfile) #read from datadir/test.csv, write into datadir/stem_out

