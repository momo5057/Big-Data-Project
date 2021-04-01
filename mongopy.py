from pymongo import MongoClient
import pprint
import json

from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt


#connect to mongo client
client = MongoClient()
print(client)

# #creates a new database or uses existing one
db = client.twitterCollection
print(db)


#specifying which collection to use
twitterTweets = db.tweetsTwitter
print(twitterTweets)


def calculatePercentage(numerator, denominator):
	return 100 * float(numerator) / float(denominator)


consumerKey = "5aeFOUIE2u54ZJCByg9coUTyh"
consumerSecret = "HOeRP1C8AKU1lv9akRCdOfaGfLclsToBLe2mO2xaclZXbKuxi7"
accessToken = ""
accessSecret = ""

# Below 3 lines allows us to write/read find tweets of users by using it's api
auth = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
auth.set_access_token(accessToken, accessSecret)
api = tweepy.API(auth)

searchTerm = input("Enter the keyword you want to search from Twitter: ")
noOfTerms = int(input("How many tweets do you want to analyze? "))

tweets = tweepy.Cursor(api.search, q=searchTerm, lang='en').items(noOfTerms)

# print(tweets)

# result = twitterTweets.insert_one(json.dumps(tweets))

# print(result)

positive = 0
negative = 0
neutral = 0
average = 0

# Printing the tweets & saving into mongo
for tweet in tweets:
    print(tweet.text)
    string = { "tweet": tweet.text}
    # jsonString = json.dumps(string)
    # print(jsonString)
    result = twitterTweets.insert_one(string)
    analysis = TextBlob(tweet.text)
    
    if analysis.sentiment.polarity == 0:
        neutral += 1
        
    elif analysis.sentiment.polarity < 0:
        negative += 1
    elif analysis.sentiment.polarity > 0:
        positive += 1

positive = calculatePercentage(positive, noOfTerms)
negative = calculatePercentage(negative, noOfTerms)
neutral = calculatePercentage(neutral, noOfTerms)

print(positive)
print(negative)
print(neutral)


positive = format(positive, '.2f')
negative = format(negative, '.2f')
neutral = format(neutral, '.2f')

# Plotting the plots using pyplot
labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc='best')
plt.title("How people are reacting on " + searchTerm + " by analyzing " + str(noOfTerms) + " Tweets!")
plt.show()


for doc in twitterTweets.find():
    pprint.pprint(doc)


client.close()
