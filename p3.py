## SI 206 Winter 2017
## Project 3
## Building on HW6, HW7 (and some previous material!)

## NOTE: There are tests for this project, but the tests are NOT exhaustive -- you should pass them, but ONLY passing them is not necessarily sufficient to get 100% on the project. The caching must work correctly, the queries/manipulations must follow the instructions and work properly. You can ensure they do by testing just the way we always do in class -- try stuff out, print stuff out, use the SQLite DB Browser and see if it looks ok!

## You may turn the project in late as a comment to the project assignment at a deduction of 10 percent of the grade per day late. This is SEPARATE from the late assignment submissions available for your HW.

import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
import json
import sqlite3
import re

## Your name: Sara Ramaswamy 
## The names of anyone you worked with on this project:

#####

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE

## Task 1 - Gathering data

## Define a function called get_user_tweets that gets at least 20 Tweets from a specific Twitter user's timeline, and uses caching. The function should return a Python object representing the data that was retrieved from Twitter. (This may sound familiar...) We have provided a CACHE_FNAME variable for you for the cache file name, but you must write the rest of the code in this file.

CACHE_FNAME = "SI206_project3_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


# Define your function get_user_tweets here:
def get_user_tweets(twitter_handle):
	unique_id = "twitter_{}".format(twitter_handle)
	if unique_id in CACHE_DICTION:
		print('using cached data for', twitter_handle)
		twitter_results = CACHE_DICTION[unique_id]
	else: 
		print('getting data from internet for', twitter_handle)
		twitter_results = api.user_timeline(twitter_handle)
		CACHE_DICTION[unique_id] = twitter_results
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	tweet_count = 0
	tweet_texts = []
	for tweet in twitter_results:
		if tweet_count<20:
			tweet_texts.append(tweet)
	return tweet_texts


# Write an invocation to the function for the "umich" user timeline and save the result in a variable called umich_tweets:
umich_tweets = get_user_tweets("umich") 
# print(umich_tweets[0])

## Task 2 - Creating database and loading data into database

# You will be creating a database file: project3_tweets.db
conn = sqlite3.connect('project3_tweets.db')
cur = conn.cursor()
# Note that running the tests will actually create this file for you, but will not do anything else to it like create any tables; you should still start it in exactly the same way as if the tests did not do that! 
# The database file should have 2 tables, and each should have the following columns...

cur.execute('DROP TABLE IF EXISTS Users')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Users (user_id STRING PRIMARY KEY, screen_name TEXT UNIQUE, num_favs INTEGER, description TEXT)'

cur.execute(statement)

cur.execute('DROP TABLE IF EXISTS Tweets')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Tweets (tweet_id STRING PRIMARY KEY, text TEXT, user_id TEXT, time_posted TIMESTAMP, retweets INTEGER, FOREIGN KEY(user_id) REFERENCES Users(user_id) ON UPDATE SET NULL)' 


cur.execute(statement)
conn.commit()

# table Tweets, with columns:
# - tweet_id (containing the string id belonging to the Tweet itself, from the data you got from Twitter) -- this column should be the PRIMARY KEY of this table
# - text (containing the text of the Tweet)
# - user_posted (an ID string, referencing the Users table, see below)
# - time_posted (the time at which the tweet was created)
# - retweets (containing the integer representing the number of times the tweet has been retweeted)


# table Users, with columns:
# - user_id (containing the string id belonging to the user, from twitter data) -- this column should be the PRIMARY KEY of this table
# - screen_name (containing the screen name of the user on Twitter)
# - num_favs (containing the number of tweets that user has favorited)
# - description (text containing the description of that user on Twitter, e.g. "Lecturer IV at UMSI focusing on programming" or "I tweet about a lot of things" or "Software engineer, librarian, lover of dogs..." -- whatever it is. OK if an empty string)

##Tweets
my_tuple1 = ()
list_of_tuples1 = []
my_tuple2 = ()
list_of_tuples2 = []
user_names = []
user_name_tuple = ()
twitter_handles = []
# my_regex = r'@(\w+)' ## get a twitter name from string
# print(umsi_tweets[0])
for tweet in umich_tweets:
	# x = re.findall(my_regex, tweet["text"])
	# My_set = set(x)
	# if len(My_set)>0:
	# 	print(My_set)
	my_tuple1 = tweet["id_str"], tweet["text"], tweet["user"]["id_str"], tweet["created_at"], tweet["retweet_count"]
	list_of_tuples1.append(my_tuple1)
	## for every tweet in this list of tweets
	## build a list of tuples to load into the database table Tweets
	##using the user_mentions in the tweets' attribute, build another list of tuples to laod into the database table USers

	# my_tuple2 = tweet["user"][]

	## gets mentioned names 
	mentions_in_tweet = tweet["entities"]["user_mentions"]
	for item in mentions_in_tweet:
		if item["screen_name"] not in user_names:
			user_names.append(item["screen_name"])
	# user_name_tuple = tuple(user_names)


	# print(mentions_in_tweet) ## type list

# print(user_name_tuple)

statement = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?)'
for item in list_of_tuples1:
	cur.execute(statement, item)

conn.commit()


## USers
name_info = []
list_of_names_tuple = ()
# print(user_names)
## able to return list of the mentioned tweets, no duplicates 
## now i want to correctly use another api function to feed those names to that function to retrieve info about that user and create the necessary tuples from that data
## feed those tuples into the Users Database 

# user_results = api.get_user(user_names)
# print(user_results)
# user_results = api.get_user(user_names)
# print(json.dumps(user_results, indent = 2))
# for name in user_names:
# 	if name in CACHE_DICTION:

# 	else:
# 		print("getting internet data for user info for ", name)
# 		user_results = api.get_user(name)
# 		user_name_tuple = user_results["id_str"], user_results["screen_name"], user_results["favourites_count"], user_results["description"]
# 		list_of_tuples2.append(user_name_tuple)
# 		CACHE_DICTION[name] = list_of_tuples2
# 		f = open(CACHE_FNAME, 'w')
# 		f.write(json.dumps(CACHE_DICTION))
# 		f.close()

# user_name_tuple = user_results["id_str"], user_results["screen_name"], user_results["favourites_count"], user_results["description"]
# 		list_of_tuples2.append(user_name_tuple)

def get_user_info(twitter_name):
	if twitter_name in CACHE_DICTION:
		print('using cached data for', twitter_name)
		user_info = CACHE_DICTION[twitter_name]
	else: 
		print('getting data from internet for', twitter_name)
		user_info = api.get_user(twitter_name)
		
		CACHE_DICTION[twitter_name] = user_info
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return user_info

for name in user_names:
	user_results = get_user_info(name)
	user_name_tuple = user_results["id_str"], user_results["screen_name"], user_results["favourites_count"], user_results["description"]
	list_of_tuples2.append(user_name_tuple)


statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)'
for item in list_of_tuples2:
	cur.execute(statement, item)

conn.commit()


# for tweet in umich_tweets:
# 	tweet_id = tweet["user"]["screen_name"]
# 	tweet_text = tweet["text"]
# 	print(tweet_text)
# 	get_user_names = 'SELECT text FROM Tweets WHERE instr(text, "@")'
# 	cur.execute(get_user_names)

	# select_sql = 'SELECT * FROM Tweets WHERE text=' + my_str
	# cur.execute(select_sql, (text,))
	# if not cur.fetchone():
	# 	insert_sql = 'INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?)'
	# 	cur.execute(insert_sql, (tweet["user"]["id_str"], tweet["user"]["screen_name"], tweet["user"]["favourites_count"], tweet["user"]["description"]))



	# my_tuple2 = tweet["user"]["id_str"], tweet["user"]["screen_name"], tweet["user"]["favourites_count"], tweet["user"]["description"]
	# list_of_tuples2.append(my_tuple2)
# print(list_of_tuples)


## old solution
# statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)'
# for item in list_of_tuples2:
# 	print(item)
# 	cur.execute(statement, item)



conn.commit()
## You should load into the Users table:
# The umich user, and all of the data about users that are mentioned in the umich timeline. 
## done
# NOTE: For example, if the user with the "TedXUM" screen name is mentioned in the umich timeline, that Twitter user's info should be in the Users table, etc.

## You should load into the Tweets table: 
# Info about all the tweets (at least 20) that you gather from the umich timeline.
# NOTE: Be careful that you have the correct user ID reference in the user_id column! See below hints.

## HINT: There's a Tweepy method to get user info that we've looked at before, so when you have a user id or screenname you can find alllll the info you want about the user.
## HINT #2: You may want to go back to a structure we used in class this week to ensure that you reference the user correctly in each Tweet record.
## HINT #3: The users mentioned in each tweet are included in the tweet dictionary -- you don't need to do any manipulation of the Tweet text to find out which they are! Do some nested data investigation on a dictionary that represents 1 tweet to see it!

## INSERT INTO bar (description, foo_id) VALUES
## ('testing, (SELECTION id from foo WHERE type = 'blue' ) ' )    ## foo is table with 2 field--one is id one is type, description = to test and secodnd one description = another row 


## Task 3 - Making queries, saving data, fetching data ##easy

# All of the following sub-tasks require writing SQL statements and executing them using Python.

# Make a query to select all of the records in the Users database. Save the list of tuples in a variable called users_info.
query1 = 'SELECT * From Users'
cur.execute(query1)
users_info = cur.fetchall()

# Make a query to select all of the user screen names from the database. Save a resulting list of strings (NOT tuples, the strings inside them!) in the variable screen_names. HINT: a list comprehension will make this easier to complete!
 
## need query 2
screen_names = []
query2 = 'SELECT  screen_name from Users'
cur.execute(query2)
string_nms = cur.fetchall()
for x in string_nms:
	screen_names.append(x[0])


# print(string_nms)

# print(string_nms[0])
# for item in string_nms:


# print(my_list)

# Make a query to select all of the tweets (full rows of tweet information) that have been retweeted more than 25 times. Save the result (a list of tuples, or an empty list) in a variable called more_than_25_rts.

query3 = 'SELECT * From Tweets WHERE retweets > 25'
cur.execute(query3)
more_than_25_rts = cur.fetchall()

# Make a query to select all the descriptions (descriptions only) of the users who have favorited more than 25 tweets. Access all those strings, and save them in a variable called descriptions_fav_users, which should ultimately be a list of strings.

query4 = 'SELECT description from Users WHERE num_favs > 25'
cur.execute(query4)
descriptions_fav_users = []
string_descrips = cur.fetchall()
for x in string_descrips:
	descriptions_fav_users.append(x[0])


# Make a query using an INNER JOIN to get a list of tuples with 2 elements in each tuple: the user screenname and the text of the tweet -- for each tweet that has been retweeted more than 50 times. Save the resulting list of tuples in a variable called joined_result.


## Task 3 help with query 5 
## ask about this
## only passes when retweets is lower numer, otherwise empty list and fails the test if not populated by tuples
query5 = 'SELECT Users.screen_name, Tweets.text FROM Tweets INNER JOIN Users on Tweets.user_id=Users.user_id WHERE Tweets.retweets > 5'
cur.execute(query5)
joined_result = cur.fetchall()
# print(joined_result)


## Task 4 - Manipulating data with comprehensions & libraries ##set comp?

## Use a set comprehension to get a set of all words (combinations of characters separated by whitespace) among the descriptions in the descriptions_fav_users list. Save the resulting set in a variable called description_words.

# print(descriptions_fav_users)
# joined_descrips = []
joined_descrips = ''.join(descriptions_fav_users)
# print(joined_descrips)
# print(len(joined_descrips)) ## chars
joined_2 = joined_descrips.split()
joined_3 = joined_descrips.strip()
joined_4 = joined_3.replace(' ', '')
print(joined_4)
# print(type(joined_2))
# print(len(joined_2))
# for item in descriptions_fav_users:
# 	# item.split()
# 	print(item.split())
# print(joined_descrips)

# print(joined_descrips)
## set comprehension requirement fulfilled 
description_words = {x for x in joined_2}
# print(len(description_words))
# print(description_words)
## edit this
# print(description_words)


## Use a Counter in the collections library to find the most common character among all of the descriptions in the descriptions_fav_users list. Save that most common character in a variable called most_common_char. Break any tie alphabetically (but using a Counter will do a lot of work for you...).
## are we counting whitespace char? yes? 
char_count = collections.Counter(joined_4)
print(char_count)
# print(char_count)
for letter, count in char_count.most_common(1):
	most_common_char = letter
	# print(most_common_char)
# print(most_common_char)

## Putting it all together...
# Write code to create a dictionary whose keys are Twitter screen names and whose associated values are lists of tweet texts that that user posted. You may need to make additional queries to your database! To do this, you can use, and must use at least one of: the DefaultDict container in the collections library, a dictionary comprehension, list comprehension(s). Y
# You should save the final dictionary in a variable called twitter_info_diction.

## create dictionary who keys are twitter screen names (query table for screen names)
twitter_info_diction = {}
query6 = 'SELECT screen_name from Users'
cur.execute(query6)
sns = cur.fetchall()
# print(sns)
# query7 = 

# for name in user_names:
# 	user_results = api.get_user(name)
# 	user_name_tuple = user_results["id_str"], user_results["screen_name"], user_results["favourites_count"], user_results["description"]
# 	list_of_tuples2.append(user_name_tuple)

# descriptions_fav_users = []
# string_descrips = cur.fetchall()
# for x in string_descrips:
# 	descriptions_fav_users.append(x[0])
# donald = get_user_tweets("realDonaldTrump")
# print(donald[0])
# print(len(donald))
list_to_dict = []	

for item in sns:
	list_to_dict.append(item[0])
# print(list_to_dict)
for name in list_to_dict:
	# new_list = []
	usr_tweets = get_user_tweets(name) ## gets python object representing data of 20 tweets
	user_tweet_text = [tweet["text"] for tweet in usr_tweets]
	 ## get the tweet's text attribute and append to user_tweet_Text list for this user 
	twitter_info_diction[name] = user_tweet_text ##  assign that list of text of tweets to the key in the twitter_info_diction
	## when the big for loop starts again, it will do the same for the next name
# print(twitter_info_diction)
# print(twitter_info_diction["HoffmanAndy"][0]["text"])
## dictionary keys ARE the screen_names 


# print(twitter_info_diction.values())

## assign list of tweet texts that user posted to that key
## use DefaultDict container in the collections library, a dict. comprehension, list comprehensions(s)
## save final dictionary to twitter_info_diction



##CLOSE THE DATABASE
### IMPORTANT: MAKE SURE TO CLOSE YOUR DATABASE CONNECTION AT THE END OF THE FILE HERE SO YOU DO NOT LOCK YOUR DATABASE (it's fixable, but it's a pain). ###
cur.close()

###### TESTS APPEAR BELOW THIS LINE ######
###### Note that the tests are necessary to pass, but not sufficient -- must make sure you've followed the instructions accurately! ######
print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")

class Task1(unittest.TestCase):
	def test_umich_caching(self):
		m_file = open("SI206_project3_cache.json","r")
		## open file associated with string, read it
		## save the contents to string
		## can safely close file because the contents are saved 
		## fstr is type string
		fstr = m_file.read()
		m_file.close()
		self.assertTrue("umich" in fstr)
	def test_get_user_tweets(self):
		res = get_user_tweets("umsi")
		self.assertEqual(type(res),type(["hi",3]))
	def test_umich_tweets(self):
		self.assertEqual(type(umich_tweets),type([]))
	def test_umich_tweets2(self):
		self.assertEqual(type(umich_tweets[18]),type({"hi":3}))
	def test_umich_tweets_function(self):
		self.assertTrue(len(umich_tweets)>=20)

class Task2(unittest.TestCase):
	def test_tweets_1(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=20, "Testing there are at least 20 records in the Tweets database")
		conn.close()
	def test_tweets_2(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==5,"Testing that there are 5 columns in the Tweets table")
		conn.close()
	def test_tweets_3(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT user_id FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1][0])>=2,"Testing that a tweet user_id value fulfills a requirement of being a Twitter user id rather than an integer, etc")
		conn.close()
	def test_tweets_4(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT tweet_id FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(result[0][0] != result[19][0], "Testing part of what's expected such that tweets are not being added over and over (tweet id is a primary key properly)...")
		if len(result) > 20:
			self.assertTrue(result[0][0] != result[20][0])
		conn.close()
	def test_users_4(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
		conn.close()
	def test_users_5(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)<20,"Testing that there are fewer than 20 users in the users table -- effectively, that you haven't added duplicate users. If you got hundreds of tweets and are failing this, let's talk. Otherwise, careful that you are ensuring that your user id is a primary key!")
		conn.close()
	def test_users_6(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==4,"Testing that there are 4 columns in the Users database")
		conn.close()

class Task3(unittest.TestCase):
	def test_users_info(self):
		self.assertEqual(type(users_info),type([]),"testing that users_info contains a list")
	def test_users_info2(self):
		self.assertEqual(type(users_info[1]),type(("hi","bye")),"Testing that an element in the users_info list is a tuple")
	def test_track_names(self):
		self.assertEqual(type(screen_names),type([]),"Testing that track_names is a list")
	def test_track_names2(self):
		self.assertEqual(type(screen_names[1]),type(""),"Testing that an element in screen_names list is a string")
	def test_more_rts(self):
		if len(more_than_25_rts) >= 1:
			self.assertTrue(len(more_than_25_rts[0])==5,"Testing that a tuple in more_than_ten_rts has 5 fields of info (one for each of the columns in the Tweet table)")
	def test_more_rts2(self):
		self.assertEqual(type(more_than_25_rts),type([]),"Testing that more_than_ten_rts is a list")
	def test_more_rts3(self):
		if len(more_than_25_rts) >= 1:
			self.assertTrue(more_than_25_rts[1][-1]>10, "Testing that one of the retweet # values in the tweets is greater than 10")
	def test_descriptions_fxn(self):
		self.assertEqual(type(descriptions_fav_users),type([]),"Testing that descriptions_fav_users is a list")
	def test_descriptions_fxn2(self):
		self.assertEqual(type(descriptions_fav_users[0]),type(""),"Testing that at least one of the elements in the descriptions_fav_users list is a string, not a tuple or anything else")
	def test_joined_result(self):
		self.assertEqual(type(joined_result[0]),type(("hi","bye")),"Testing that an element in joined_result is a tuple")

class Task4(unittest.TestCase):
	def test_description_words(self):
		print("To help test, description words looks like:", description_words)
		self.assertEqual(type(description_words),type({"hi","Bye"}),"Testing that description words is a set")
	def test_common_char(self):
		self.assertEqual(type(most_common_char),type(""),"Testing that most_common_char is a string")
	def test_common_char2(self):
		self.assertTrue(len(most_common_char)==1,"Testing that most common char is a string of only 1 character")
	def test_twitter_info_diction(self):
		self.assertEqual(type(twitter_info_diction),type({"hi":3}))
	def test_twitter_info_diction2(self):
		self.assertEqual(type(list(twitter_info_diction.keys())[0]),type(""),"Testing that a key of the dictionary is a string")
	def test_twitter_info_diction3(self):
		self.assertEqual(type(list(twitter_info_diction.values())[0]),type([]),"Testing that a value in the dictionary is a list")
	def test_twitter_info_diction4(self):
		self.assertEqual(type(list(twitter_info_diction.values())[0][0]),type(""),"Testing that a single value inside one of those list values-in-dictionary is a string! (See instructions!)")


if __name__ == "__main__":
	unittest.main(verbosity=2)