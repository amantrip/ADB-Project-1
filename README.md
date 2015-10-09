# ADB-Project-1

COMS E6111 Advance Database Systems
Project 1

a) Akhilesh Mantripragada(am4227) and Yehuda Stuchins (yss2117)

b) queryExpander.py, utilities.py, transcript.txt, Makefile

c) Run "$make". Then simply enter the desired precision and query when prompted.

d) The basic outline of the program is in the main function in queryExpander.py, while most of the functionality is in the functions in utilities.py. The program prompts the user for input for the precision and the query, then it sends the query to Bing, parses the result and requests feedback from the user on the first ten results. Then, if the precision is below the requested value, it determines the two additional words to add to the query and then starts the process over again. 
To illustrate the while in more detail:
-  we first query the BING API and store results
-  show results to the user and get feedback. While getting feedback we remove any characters from the document that will unncessasry for the next iteration.
- Then we generate the list of terms for each document and update a term in a doc's score with normalized term frequency while also indexing by term.
- Then we apply the inverse dFrequency to term score
- Divide relevant and non-relevant term scores
- Using th rocchio's algorithm, we get the master term scores.
- Finally we update the query with the best two terms.

Note: We used Python's dictionary data type as well as Python's list data type. We stored the query terms and the stop words in lists (qTerms and stopWords). The bing query returned documents of json type and are converted into a list of dictionaries. 

e)
We implemented query-expasion method based on Rocchio's algorithm (from chapters 9 and 6 of the Introduction to Information Retrieval textbook respectively).
The query expansion method includes: 
- Term score compilation for each document.
All Scores for terms intially set to 0, then we update the term score for each term in the title and description of a document with normalized term frequency. We do the follwoing for each document by incrementing each term's score by 1 divided by the document's term count (1/word count) for each term in the document's term list. Finally we update the term score for each term in title/description of document with Inverse Document Frequency. This is done for each document by multiplying each term's score bylog(returned documents / inverse dFrequency).
- Relevant/NonRelevant Term Score 
Scores for all terms are intially set to 0 for both relevant and nonrelevant dictionaries. We then generate relevant document term scores and finally generate nonrelevant document term score
- Master Term Score Compilation
We first set scores for all terms intially to 0 for master dictionary. Then while we keep track of top 2 non-query term scores, we calculate the master term score for terms in the relevant dictionary. We set the term's score to the Rocchio normalized relevant term score by setting it to the relevant term score divided by the number of relevant documents multiplied by the Rocchio Beta constant. We then decrement the term's score by the Rocchio normalized nonrelevant term score by subsracting the nonrelevant term score divided by the number of nonrelevant documents multiplied by the Rocchio Gamma constant (we used .15). Finally we weight previous query terms higher.
- Query Generation
We first add terms with 2 highest master term scores to query and then we sort query by master term score.
f) QgPWn9g/wi5g0BrHFTheQNwEjD+/m98WcIi8ps2G6V8=