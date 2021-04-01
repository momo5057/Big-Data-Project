from pymongo import MongoClient
import pprint

#connect to mongo client
client = MongoClient()
print(client)

#creates a new database or uses existing one
db = client.tweetsdb
#db = client["tweetsdb"]
print(db)


#example json with tweet
tweet1 = {
     "title": "Working With JSON Data mongo",
     "author": "Lucas",
     
 }

#specifying which collection to use
tweets = db.tweets
print(tweets)


#insert document into collection
result = tweets.insert_one(tweet1)

#to insert many documents at the same time
#new_result = tweets.insert_many([tweet2, tweet3])

for doc in tweets.find():
    pprint.pprint(doc)


client.close()