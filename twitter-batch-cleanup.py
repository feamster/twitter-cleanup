#!/usr/local/bin/python

#################################################################
# Clean up old tweets based on downloaded Twitter archive.
# Nick Feamster
# Created: July 31, 2018
# Updated: December 18, 2020
#################################################################

import tweepy
import json
import re
import datetime
import dateutil.parser
import sys
import time


#################################################################
# Fill in these values by creating an app on the Twitter site that has access to your account

with open('config.json', 'rt', encoding='utf-8') as data_file:
    json_data = data_file.read()
credentials = json.loads(json_data)[0]
files = json.loads(json_data)[1]

user = credentials['user']
consumer_key = credentials['consumer_key']
consumer_secret = credentials['consumer_secret']
access_key = credentials['access_key']
access_secret = credentials['access_secret']

#################################################################
# This is the 'tweet.js' and 'like.js' file that you download from the Twitter site by requesting your data.

# Note: the downloaded files have a variable assignment at the beginning which the python JSON parser cannot grok.
# That variable assignment needs to be deleted so that the only thing in the file is the json array ("[{ ...}]".

tfile = files['tweets']
lfile = files['likes']


#################################################################
# Step 0: Login

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print("Authenticated as: %s" % api.me().screen_name)

#################################################################
# Step 1: Mark for Deletion

with open(tfile, 'rt', encoding='utf-8') as data_file:
    json_data = data_file.read()

tweets = json.loads(json_data)

# ### Mark For Deletion

tweets_marked = []

for t in tweets:
    tweet = t['tweet']

    # Is it a reply?
    try:
        reply = tweet['in_reply_to_user_id']
    except KeyError as e:
        reply = None

    # Is it a retweet?
    retweeted = tweet['retweeted']

    # Get the ID, text, and date of the Tweet from the JSON
    id = tweet['id_str']
    tweet_text = tweet['full_text']
    tweet_date = dateutil.parser.parse(tweet['created_at']).date()

    # How old is the Tweet?
    tweet_age = (datetime.date.today() - tweet_date).days
    #print tweet_date, tweet_age

    # If it is a reply, mark it for deletion.
    if reply is not None:
        print (reply, "reply marked for deletion")
        tweets_marked.append(id)
        continue

    # If it is a retweet, mark it for deletion.
    if re.match(r'^RT', tweet_text):
        print(tweet_text, "marked for deletion")
        tweets_marked.append(id)        
        continue

    # mark old tweets. adjust based on time range of interest.
    if tweet_age > (365*1) and tweet_age < (365*3):
        print(tweet_age, "days old", tweet_text)
        delt = sys.stdin.readline()
        if re.match(r'^y', delt):
            print("marked for deletion")
            tweets_marked.append(id)
        if re.match(r'b', delt):
            print("breaking")
            break

#################################################################
# Step 2: Delete all marked IDs.

# build list of marked status IDs
delete_count = 0
#delete marked tweets by status ID
for status_id in tweets_marked:
    try:
        api.destroy_status(int(status_id))
        print(status_id, 'deleted!')
        delete_count += 1
    except tweepy.error.TweepError as e:
        print(status_id, 'could not be deleted: ', e.reason)
print(delete_count, 'tweets deleted.')


#################################################################
# Step 3: Batch un-like all liked Tweets.
# This is the 'like.js' file that you download from the Twitter site

with open(lfile, 'r') as data_file:
    json_data = data_file.read()

likes = json.loads(json_data)


for tweet_liked in likes:
    status_id = tweet_liked['like']['tweetId']
    fullText = tweet_liked['like']['fullText']
    #tweet = api.get_status(status_id)
    #print(tweet)
    try:
        api.destroy_favorite(int(status_id))
        print(status_id, 'like removed!')
        delete_count += 1
    except tweepy.error.TweepError as e:
        print(status_id, 'could not be un-liked: ', e.reason)

print(delete_count, 'likes removed.')
