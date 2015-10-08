import base64
import json
import urllib2
from collections import defaultdict
from math import log
import utilities

#run the program
def main():
	print "Enter precision:",
	targetPrecision = float(raw_input())
	precision = -1.0

	print "Enter Query:",
	inputQuery = raw_input()
	qTerms = inputQuery.split()

	bingAccountKey = "QgPWn9g/wi5g0BrHFTheQNwEjD+/m98WcIi8ps2G6V8="

	while(precision < targetPrecision):

		#Print bing API key
		print "Client Key\t= " + bingAccountKey

		#Print query terms
		query = qTerms[0]
		for qTerm in xrange(len(qTerms) - 1):
			query += (" "+qTerms[qTerm + 1])

		print "Query\t\t= " + query
		query = query.replace(" ", "+")

		#Print precision
		print "Precision\t= " + str(targetPrecision)

		#Print URL
		url = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27" + query + "%27&$top=10&$format=json"
		print "URL: " + url

		#query the API and get docs
		documents = utilities.search(query, url, bingAccountKey)

		#show results and get feedback
		documents = utilities.getFeedback(documents)

		#show new results
		print "======================"
		print "FEEDBACK SUMMARY"
		print "Query " + query.replace("+", " ")

		#intermediate check 
		if utilities.checkTargetPrecision(documents, targetPrecision):
			break

		print "Indexing results..."

		dFrequency = defaultdict(list)
		for index in xrange(len(documents)):
			#initialize scores to 0
			documents[index]['score'] = defaultdict(int)

			#get rid of characters
			documents[index] = utilities.removeCharacters(documents[index])

			#terms from description and title of document
			terms = utilities.getTerms(documents[index])

			wCount = float(len(terms))

			for term in terms:
				documents[index]['score'][term] = documents[index]['score'][term] + 1/wCount

				if(len(dFrequency[term]) is 0):
						dFrequency[term] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

				dFrequency[term][index] = 1


		dFrequency = utilities.computeDocumentFrequency(dFrequency, len(documents))

		#use the document frequency to update the scores
		documents = utilities.documentFrequencyTermScore(documents, dFrequency)

		#we then create to dicts: one that is relevant and the other that is not
		dRelevant, dNRelevant = utilities.divideDictionary(documents)

		#run Rocchio Algorithm
		mDict = utilities.getMasterDictionary(dRelevant, dNRelevant, documents, qTerms)

		#get the two most important terms to add
		bestTerm1, bestTerm2 = utilities.getBestTerms(mDict, qTerms)

		print "Augmenting by "+ bestTerm1 + " " + bestTerm2

		if(bestTerm1 != " "):
			qTerms.append(bestTerm1)
			if(bestTerm2 != " "):
					qTerms.append(bestTerm2)
		else:
			print "No further augumentation!"
			break			

		def score(m): return mDict[m.lower()]	
		qTerms.sort(key=score, reverse=True)


# call the main function
main()	