import base64
import json
import urllib2
from collections import defaultdict
from math import log

stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an',
                  'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot',
                  'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from',
                  'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however',
                  'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may',
                  'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often',
                  'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should',
                  'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these',
                  'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what',
                  'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet',
                  'you', 'your', 'age', 'concern', 'about' , 'above' , 'after' , 'again' , 'against' ,'all' ,
                    'am' ,
                    'an' ,
                    'and' ,
                    'any' ,
                    'are' ,
                    'aren' ,
                    'as' ,
                    'at' ,
                    'be' ,
                    'because' ,
                    'been' ,
                    'before' ,
                    'being' ,
                    'below' ,
                    'between' ,
                    'both' ,
                    'but' ,
                    'by' ,
                    'can' ,
                    'cannot',
                    'could' ,
                    'couldn' ,
                    'did' ,
                    'didn' ,
                    'do' ,
                    'does' ,
                    'doesn' ,
                    'doing' ,
                    'don' ,
                    'down' ,
                    'during' ,
                    'each' ,
                    'few' ,
                    'for' ,
                    'from' ,
                    'further' ,
                    'had' ,
                    'hadn' ,
                    'has' ,
                    'hasn' ,
                    'have' ,
                    'haven' ,
                    'having' ,
                    'he' ,
                    'her' ,
                    'here' ,
                    'here' ,
                    'hers' ,
                    'herself' ,
                    'him' ,
                    'himself' ,
                    'his' ,
                    'how' ,
                    'how' ,
                    'if' ,
                    'in' ,
                    'into' ,
                    'is' ,
                    'isn' ,
                    'it' ,
                    'its' ,
                    'itself' ,
                    'let' ,
                    'me' ,
                    'more' ,
                    'most' ,
                    'mustn' ,
                    'my' ,
                    'myself' ,
                    'no' ,
                    'nor' ,
                    'not' ,
                    'of' ,
                    'off' ,
                    'on' ,
                    'once' ,
                    'only' ,
                    'or' ,
                    'other' ,
                    'ought' ,
                    'our' ,
                    'ours' ,
                    'ourselves' ,
                    'out' ,
                    'over' ,
                    'own' ,
                    'same' ,
                    'shan' ,
                    'she' ,
                    'should' ,
                    'shouldn' ,
                    'so' ,
                    'some' ,
                    'such' ,
                    'than' ,
                    'that' ,
                    'the' ,
                    'their' ,
                    'theirs' ,
                    'them' ,
                    'themselves' ,
                    'then' ,
                    'there' ,
                    'these' ,
                    'they' ,
                    'this' ,
                    'those' ,
                    'through' ,
                    'to' ,
                    'too' ,
                    'under' ,
                    'until' ,
                    'up' ,
                    'using',
                    'very' ,
                    'was' ,
                    'wasn' ,
                    'we' ,
                    'were' ,
                    'weren' ,
                    'what' ,
                    'when' ,
                    'where' ,
                    'which' ,
                    'while' ,
                    'who' ,
                    'whom' ,
                    'why' ,
                    'with' ,
                    'would' ,
                    'wouldn' ,
                    'you' ,
                    'your' ,
                    'yours' ,
                    'yourself' ,
                    'yourselves' ]


def search(query, url, accountKey):

	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	request = urllib2.Request(url, headers = headers)
	response = urllib2.urlopen(request)

	content = response.read()
	results = json.loads(content)

	return results['d']['results']


def getFeedback(documents):
	
	print "Total number of results : " + str(len(documents))
	print "Bing Search Results:"
	print "========================"

	for index in xrange(len(documents)):

		print "Result", index+1
		print "["
		print " Title: " + documents[index]['Title'].encode('ascii', 'replace')
		print " Description: " + documents[index]['Description'].encode('ascii', 'replace')
		print " Url: " + documents[index]['Url'].encode('ascii', 'replace')
		print "]\n"

		answer = ""

		while answer is not "Y" and answer is not "y" and answer is not "N" and answer is not "n":
			print "Relevant (Y/N)?",
			answer = raw_input()
			if answer is "Y" or answer is "y":
				documents[index]['relevant'] = "Y"
			else:
				documents[index]['relevant'] = "N"
	return documents
	
def getRelevantCount(documents):
	
	count = 0
	for index in xrange(len(documents)):
		if documents[index]['relevant'] is 'Y':
			count = count + 1

	return count
						

def checkTargetPrecision(docs, precision):
	relevantCount = getRelevantCount(docs)
	nonrelevantCount = len(docs) - relevantCount
	currentPrecision = float(relevantCount) / len(docs)
	print "Precision " + str(currentPrecision)
	if (currentPrecision >= precision):
		print "Desired precision reached, done"
		return True
	else:
		print "Still below the desired precision of " + str(precision)
		return False


def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

# Removes unnecessary characters from a string s
def removeChars(s):
	s = s.replace('.', '')
	s = s.replace(',', '')
	s = s.replace('&', '')
	s = s.replace('\'', '')
	s = s.replace('!', '')
	s = s.replace('\"', '')
	s = s.replace('?', '')
	s = s.replace('@', '')
	s = removeNonAscii(s)
	return s

def removeCharacters(doc):
	# From description
	doc['Description'] = removeChars(doc['Description'])
	# From title
	doc['Title'] = removeChars(doc['Title'])

	# Make lowercase
	doc['Description'] = doc['Description'].lower()
	doc['Title'] = doc['Title'].lower()

	return doc


def getTerms(doc):
	terms = doc['Description'].split()
	terms = terms + doc['Title'].split()
	return terms


def computeDocumentFrequency(df, dCount):
	for key in df:
		count = 0
		for i in xrange(dCount):
			count = count + df[key][i]
		df[key][10] = count
	return df


def documentFrequencyTermScore(docs, df):
	for i in xrange(len(docs)):
		for key in docs[i]['score']:
			docs[i]['score'][key] = docs[i]['score'][key] * log(10./df[key][10])
	return docs


def divideDictionary(docs):
	relevant = defaultdict(int)
	nonrelevant = defaultdict(int)
	for i in xrange(len(docs)):
		if docs[i]['relevant'] == 'Y':
			for key in docs[i]['score']:
				relevant[key] = relevant[key] + docs[i]['score'][key]
		else:
			for key in docs[i]['score']:
				nonrelevant[key] = nonrelevant[key] + docs[i]['score'][key]
	return relevant, nonrelevant


# Merge term scores from relevant and nonrelevant dictionaries into
# 1 dictionary using the Rocchio algorithm
def getMasterDictionary(relevant, nonrelevant, docs, queryTerms):

	relevantCount = getRelevantCount(docs)

	master = defaultdict(int)

	for key in relevant:

		master[key] = .75*relevant[key]/relevantCount
		master[key] = master[key] - .15*nonrelevant[key]/(len(docs)-relevantCount)
		notYetATerm = True

		for term in queryTerms:
			if key == term.lower():
				notYetATerm = False

	for term in queryTerms:
		master[term.lower()] = 1

	return master


def getBestTerms(master, queryTerms):
	max1Score = 0
	max2Score = 0
	max1Term = ""
	max2Term = ""

	for key in master:
		notYetATerm = True
		# Make sure key is not already a query term
		for term in queryTerms:
			if key == term.lower():
				notYetATerm = False

		# Check if key not a stop word has a high enough score to add to query
		if (notYetATerm):
			if (master[key] > max1Score and key not in stopWords):
				newMax2 = max1Score
				newMax2Term = max1Term
				max1Score = master[key]
				max1Term = key
				max2Score = newMax2
				max2Term = newMax2Term
			elif (master[key] > max2Score and key not in stopWords):
				max2Score = master[key]
				max2Term = key

	return max1Term, max2Term


