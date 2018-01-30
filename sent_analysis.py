import json, re
from nltk import word_tokenize
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def split(paragraph):
    ''' break a paragraph into sentences
        and return a list '''
    # to split by multile characters
    #   regular expressions are easiest (and fastest)
    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList

def safe_get(array, idx):
    try:
	return array[idx]
    except IndexError:
	return ""

def extract_related_sentence(review, keywords):
    sentences = split(review)
    exact, extend = "", ""
    for idx, sentence in enumerate(sentences):
        words = word_tokenize(sentence)
  	match = False
        for kw in keywords:
            if kw in words: 
 		match = True
		break
 	if match:
	    exact = exact + sentence
	    extend = extend + safe_get(sentences, idx-1) + '.' + sentence + '.' +safe_get(sentences, idx+1)
    return [exact.strip(), extend.strip(), review]
     
def get_sentiment_blob(s):
    # using textblob
    opinion = TextBlob(s)
    #opinion.sentiment.subjectivity
    return opinion.sentiment.polarity

def get_sentiment_bayes(s):
    # using textblob
    opinion = TextBlob(s, analyzer=NaiveBayesAnalyzer())
    #opinion.sentiment.subjectivity
    # rescale to [-1, 1]
    return (opinion.sentiment.p_pos-0.5)*2

def get_sentiment_vader(s, vsa):
    return vsa.polarity_scores(s)['compound']
 

# open keyword list
with open('keywords.txt') as f:
    lines = f.read()
keywords =  word_tokenize(lines.lower())

# load review data
data = json.load(open('data/sentiment_distance1.json'))

# result: review sentiment
sent_data = []

# vader sentiment analysis
vsa = SentimentIntensityAnalyzer()

#for idx, review in enumerate(data):
for review in data:
    # clean up outdated stuff
    if 'sentiment' in review: 
	del review['sentiment'] 
    if 'sentiment-full' in review: 
	del review['sentiment-full'] 

    # get price related sentence in exact, extended(+-1) and full text
    [exact, extend, full] = extract_related_sentence(review['text'].lower(), keywords)

    # no key word match, skip
    if exact == '': 
	continue

    # get sentiment
    review['sentiment-exact'] = get_sentiment_blob(exact) 
    review['sentiment-extend'] = get_sentiment_blob(extend) 
    review['sentiment-full'] = get_sentiment_blob(full) 

    if review['sentiment-extend'] < 0:
        print(review['text'])
        print(extend)
    	print("blob {}, bayes {}, vader {}\n\n".format(get_sentiment_blob(extend), get_sentiment_bayes(extend), get_sentiment_vader(extend, vsa)))

    # save review
    sent_data.append(review)
    
# save to json files 
with open('data/review_dis_sent.json', 'w+') as output:
    json.dump(sent_data, output, indent = 4)
