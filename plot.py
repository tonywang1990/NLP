import json
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

data = json.load(open('data/sentiment_distance1.json'))

#datetime.strptime(review['time'], "%B %d, %Y"

sentiment, sentiment_fulltext, distance, date, contrib = [], [], [], [], []
for review in data: 
    sentiment.append(review['sentiment'][0])
    sentiment_fulltext.append(review['sentiment-full'][0])
    distance.append(review['distance'])
    t = datetime.strptime(review['time'], "%B %d, %Y")
    date.append(date2num(t))
    contrib.append(int(review['contribution']))

plt.figure(1)
plt.xlabel('distance')
plt.ylabel('sentiment')
plt.plot(distance, sentiment_fulltext, 'r.')
plt.plot(distance, sentiment, 'b.')
plt.figure(2)
plt.xlabel('date')
plt.ylabel('sentiment')
plt.plot_date(date, sentiment_fulltext, 'r.')
plt.plot_date(date, sentiment, 'b.')
plt.figure(3)
plt.xlabel('contribution')
plt.ylabel('sentiment')
plt.plot(contrib, sentiment_fulltext, 'r.')
plt.plot(contrib, sentiment, 'b.')
fig = plt.figure(4)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('contribution')
ax.set_ylabel('distance')
ax.set_zlabel('sentiment')
ax.scatter(contrib, distance, sentiment)
plt.show()
