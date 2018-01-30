import json, re
from nltk import word_tokenize
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

def split(paragraph):
    ''' break a paragraph into sentences
        and return a list '''
    # to split by multile characters
    #   regular expressions are easiest (and fastest)
    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList

def get_distance(location, park):
    geolocator = Nominatim()
    if location == "":
	return -1
    try:
    	loc1 = geolocator.geocode(location, timeout=100)
    	loc2 = geolocator.geocode(park, timeout=100)
	if loc1 is not None and loc2 is not None:
	    distance = great_circle((loc1.latitude, loc1.longitude) , (loc2.latitude, loc2.longitude)).miles
	else:
	    distance = -1

    except Exception as e:
	print('Error message:\n' + str(e))
	#print('Processed upto review number {}\n'.format(i))
	if 'Too Many Requests' in str(e):
	    distance = -999
	else:
	    distance = -1
    return distance


# open keyword list
with open('keywords.txt') as f:
    lines = f.read()
#keywords = lines.lower().split()
keywords =  word_tokenize(lines.lower())

data = json.load(open('data/price_related_reviews.json'))

sent_data = []

start = 11841
#for idx, review in enumerate(data):
for idx in range(start, len(data)):
    review = data[idx]
    sentences = split(review['text'].lower())
    s = ""
    for sentence in sentences:
        words = word_tokenize(sentence)
  	match = False
        for kw in keywords:
            if kw in words: 
 		match = True
		break
 	if match:
	    s = s + sentence + " "
    if s is "": 
      	continue
    # get sentiment
    opinion = TextBlob(s)
    review['sentiment'] = (opinion.sentiment.polarity, opinion.sentiment.subjectivity)
    opinion = TextBlob(review['text'])
    review['sentiment-full'] = (opinion.sentiment.polarity, opinion.sentiment.subjectivity)
    # get distance
    dist = get_distance(review['park'], review['location'])
    if dist == -999:
	print('Processed upto {}'.format(idx))
	break
    elif dist < 0:
	print('Skipped {}'.format(idx))
    else:
        review['distance'] = dist
 	# save this review only if distance is valid 
    	sent_data.append(review)
    if idx%10 == 0:
	print('{}..'.format(idx))
    
    
# save to json files 
with open('data/sentiment_distance.json', 'a+') as output:
    json.dump(sent_data, output, indent = 4)
   

 	    
            

