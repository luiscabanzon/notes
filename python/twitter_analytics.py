# -*- encoding: utf-8 -*-

import tweepy
import time
import pandas as pd
import re
import collections
import json
from datetime import datetime, timedelta
import pickle

consumer_key =''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

_pwd_ = r"C:/data/Twitter/"

##################################
#    Save and load functions     #
##################################
def get_trending_topics():
	trends = api.trends_place(1)
	trends_list = []
	today = str(datetime.today())[:10]
	for i in trends[0]["trends"]:
		trend =  str(i["name"].encode("utf-8"))
		trends_list.append(trend)
	with open(_pwd_ + r"db/trends/" + today + "_trends.json", 'wb') as f:
		json.dump(trends_list, f)

def load_trending_topics(date):
	with open(_pwd_ + r"db/trends/" + date + "_trends.json", 'rb') as f:
		trends = json.load(f)
	return trends


def load_data(date, trending_topic):
	with open(_pwd_ + r"db/raw_data/" + date + "_" +  trending_topic, 'rb') as f:
		data = pickle.load(f)
	return data

##########################
# Analysis Main Function #
##########################
def download_tweets(trending_topic):
	last_month = str(datetime.today() - timedelta(days=30))[:10]
	today = str(datetime.today())[:10]
	tomorrow = str(datetime.today() + timedelta(days=1))[:10]
	trend = tweepy.Cursor(api.search, q=trending_topic, since=last_month, until=tomorrow, lang="en").items()
	data = []
	while True:
		try:
			data.append(trend.next())
		except tweepy.error.TweepError:
			break
		except StopIteration:
			break

	with open(_pwd_ + today + "_" + trending_topic + ".txt", 'wb') as f:
		pickle.dump(data, f)

	return data

def analysis(data, trending_topic, today = None):
	if today == None:
		today = str(datetime.today())[:10]
	data_text = ""
	for i in data:
		data_text = ' '.join([data[i].text.lower() for i in xrange(len(data))]).encode('utf-8')

	hashtags = []
	mentions = []
	for i in data:
		for j in i._json["entities"]["hashtags"]:
			hashtags.append(j["text"].encode('utf-8'))
		for j in i._json["entities"]["user_mentions"]:
			mentions.append(j["screen_name"].encode('utf-8'))

	hashtags_frequency = collections.Counter(hashtags)
	mentions_frequency = collections.Counter(mentions)


	df = pd.DataFrame(columns= ["created_at", "user", "favs", "rt", "lang", "time_zone", "text", "user_pic"])
	for entry in data:
		df = df.append(load_entry(entry), ignore_index = True)

	output = {}
	top_hashtags = hashtags_frequency.most_common(10)
	top_users = mentions_frequency.most_common(10)
	most_fav = df[df["favs"] == df["favs"].max()].head(1)
	most_rt = data[df[df["rt"] == df["rt"].max()].head(1).index[0]]
	time_zones = collections.Counter(df["time_zone"]).most_common(25)

	output["topic"] = trending_topic
	output["date"] = today
	output["len"] = str(len(df))

	output["lang"] = [[df["lang"].value_counts().index[i], str(df["lang"].value_counts().values[i])] for i in xrange(len(df["lang"].unique()))]
	output["time_zones"] = [[entry[0], str(entry[1])] for entry in time_zones]
	output["hashtags"] = [[top_hashtags[i][0], str(top_hashtags[i][1])] for i in xrange(min(10,(len(top_hashtags)-1)))]

	output["users"] = [[top_users[i][0], str(top_users[i][1])] for i in xrange(min(10,(len(top_users)-1)))]
	output["most_fav"] = {"user": str(most_fav["user"][most_fav.index[0]]), "user_pic": str(most_fav["user_pic"][most_fav.index[0]]), "text": str(most_fav["text"][most_fav.index[0]]), "favs": str(int(most_fav["favs"][most_fav.index[0]])), "rt": str(int(most_fav["rt"][most_fav.index[0]])), "created_at": str(most_fav["created_at"][most_fav.index[0]])}
	output["most_rt"] = {"user": str(most_rt.user.screen_name.encode("utf-8")), "user_id": str(most_rt.user.id),"user_pic": str(most_rt.user.profile_image_url.encode("utf-8")), "text": most_rt.text.encode("utf-8"), "tweet_id": str(most_rt.id), "favs": str(most_rt.favorite_count), "rt": str(most_rt.retweet_count), "created_at": str(most_rt.created_at)}
	
	if most_rt._json["retweeted"]:
		most_rt = most_rt.retweeted_status
		output["most_rt"] = {"user": str(most_rt.user.screen_name.encode("utf-8")), "user_id": str(most_rt.user.id),"user_pic": str(most_rt.user.profile_image_url.encode("utf-8")), "text": most_rt.text.encode("utf-8"), "tweet_id": str(most_rt.id), "favs": str(most_rt.favorite_count), "rt": str(most_rt.retweet_count), "created_at": str(most_rt.created_at)}
	else:
		output["most_rt"] = {"user": str(most_rt.user.screen_name.encode("utf-8")), "user_id": str(most_rt.user.id),"user_pic": str(most_rt.user.profile_image_url.encode("utf-8")), "text": most_rt.text.encode("utf-8"), "tweet_id": str(most_rt.id), "favs": str(most_rt.favorite_count), "rt": str(most_rt.retweet_count), "created_at": str(most_rt.created_at)}

	output["words_cloud"] = []
	words_cloud = collections.Counter(data_text.split(" ")).most_common(100)
	for word in words_cloud:
		output["words_cloud"].append(word[0])

	json_output = json.dumps(output)

	with open(_pwd_ + r"db/json/" + today + "_" + trending_topic + ".json", 'wb') as f:
		json.dump(json_output, f)

	return json_output


###########################
# COMPLEMENTARY FUNCTIONS #
###########################

def load_entry(entry):
	#row = pd.DataFrame(columns= ["created_at", "user", "favs", "rt", "lang", "text", "user_pic"])
	row = pd.Series()
	row["created_at"] = str(entry.created_at)
	row["user"] = entry.user.screen_name.encode("utf-8")
	row["favs"] = entry.favorite_count
	row["rt"] = entry.retweet_count
	row["lang"] = entry.lang.encode("utf-8")
	row["time_zone"] = get_time_zone(entry)
	row["text"] = entry.text.encode("utf-8")
	row["user_pic"] = entry.user.profile_image_url.encode("utf-8")
	
	return row

def get_time_zone(entry):
	if entry._json["user"]["time_zone"] == None:
		return "N/A"
	else:
		return entry._json["user"]["time_zone"].encode("utf-8")



def complete_process(trending_topic):
	analysis(download_tweets(trending_topic))


#################

###########################
# DAILY  DATA DOWNLOADING #
###########################

get_trending_topics()
with open(_pwd_ + r"db/trends/2016-11-02_trends.json", 'rb') as f:
    trends_list = json.load(f)

for trend_i in trends_list:
	print trend_i
    
for trend_i in trends_list:
	print str(datetime.now()) + " : START " + trend_i
	analysis(download_tweets(trend_i), trending_topic = trend_i)
	print str(datetime.now()) + " : FINISH " + trend_i
	time.sleep(60 * 15)


#########################
# TO UPDATE ALL REPORTS #
#########################
'''
from os import listdir
files = listdir(_pwd_ + r"db/raw_data")
for f in files:
	print str(datetime.now()) + " : START " + f[:-4]
	with open(_pwd_ + r"/db/raw_data/" + f, 'rb') as x:
		data = pickle.load(x)
	print str(datetime.now()) + " : LOADED " + f[:-4]
	analysis(data, f[11:-4], today = f[:10])
	print str(datetime.now()) + " : FINISH " + f[:-4]
'''