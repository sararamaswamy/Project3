# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out


## Make sure to comment with:
# Your name: Sara Ramaswamy
# The names of any people you worked with for this assignment:

# ******** #
### Useful resources for this HW:
## cached_tweepy_example.py
## HW5
## https://books.trinket.io/pfe/14-database.html and database examples from class
## Lecture 17 notes, Lecture 18 notes
# ******** #

## Instructions for this assignment can be found in this file, along with some provided structure and some provided code.

## There are 3 parts to this assignment, each of which is described below.

## There are tests for each part, but the tests are NOT exhaustive, because you may each have different tweets, etc. Make sure you check the data you get -- print it out, check the types, look in the database browser, try out your SQL queries!

## We have provided setup code for you to use Tweepy, like we did for HW5 and Project 2:

# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching, just like in Project 2.
CACHE_FNAME = "206W17_HW7_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

## [PART 1]

# Here, define a function called get_user_tweets that accepts a specific Twitter user handle (e.g. "umsi" or "umich" or "Lin_Manuel" or "ColleenAtUMSI") and returns data that represents at least 20 tweets from that user's timeline.

# Your function must cache data it retrieves and rely on a cache file!
## cached correctl because first time got info from internet and second time cached data
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
		f.close
	tweet_count = 0
	tweet_texts = []
	for tweet in twitter_results:
		if tweet_count<20:
			tweet_texts.append(tweet)
	return tweet_texts



# Note that this is a lot like work you have done already in class (but, depending upon what you did previously, may not be EXACTLY the same, so be careful your code does exactly what you want here).


conn = sqlite3.connect('tweets.db')
cur = conn.cursor()
# Write code to create/build a connection to a database: tweets.db,
# And then load all of those tweets you got from Twitter into a database table called Tweets, with the following columns in each row:
cur.execute('DROP TABLE IF EXISTS Tweets')
table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (id INTEGER PRIMARY KEY AUTOINCREMENT, '
table_spec  += 'tweet_id TEXT, author TEXT, time_posted TIMESTAMP, tweet_text TEXT, retweets INTEGER)'
cur.execute(table_spec)
## tweet_id - containing the unique id that belongs to each tweet
##[id]
## author - containing the screen name of the user who posted the tweet (note that even for RT'd tweets, it will be the person whose timeline it is)
##["user"][screen_name]
## time_posted - containing the date/time value that represents when the tweet was posted (note that this should be a TIMESTAMP column data type!)
##[created_at]
## tweet_text - containing the text that goes with that tweet##[text]
##[text]
## retweets - containing the number that represents how many times the tweet has been retweeted
##[retweet_count]

# Below we have provided interim outline suggestions for what to do, sequentially, in comments.

# Make a connection to a new database tweets.db, and create a variable to hold the database cursor.


# Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
# HINT: Remember that the time_posted column should be the TIMESTAMP data type!


# Invoke the function you defined above to get a list that represents a bunch of tweets from the UMSI timeline. Save those tweets in a variable called umsi_tweets.

umsi_tweets = get_user_tweets("umsi")
my_tuple = ()
list_of_tuples = []
# print(umsi_tweets[0])
for tweet in umsi_tweets:
	my_tuple = None, tweet["id"], tweet["user"]["screen_name"], tweet["created_at"], tweet["text"], tweet["retweet_count"]
	list_of_tuples.append(my_tuple)
	


statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for item in list_of_tuples:
	cur.execute(statement, item)

conn.commit()
# for tweet in umsi_tweets:
# 	each_tuple = (tweet["id"], tweet["screen_name"], )

# 	cur.execute(statement, tweet)
# 	'INSERT INTO Tweets (tweet_id, author, time_posted, tweet_text, retweets) VALUES (?, ?, ?, ?, ?)', ('tweet["id"]', 'tweet["user"]["screen_name"]', 'tweet["created_at"]', 'tweet["text"]', 'tweet["retweet_count"]')
# conn.commit()


# print(umsi_tweets[0].keys())
# print(umsi_tweets[0]["user"]["screen_name"])

# Use a for loop, the cursor you defined above to execute INSERT statements, that insert the data from each of the tweets in umsi_tweets into the correct columns in each row of the Tweets database table.

# statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?)'
# for t in 

# (You should do nested data investigation on the umsi_tweets value to figure out how to pull out the data correctly!)




# Use the database connection to commit the changes to the database



# You can check out whether it worked in the SQLite browser! (And with the tests.)



## [PART 2] - SQL statements

## In this part of the homework, you will write a number of Python/SQL statements to get data from the database, as directed. For each direction, write Python code that includes an SQL statement that will get the data from your database. 
## You can verify whether your SQL statements work correctly in the SQLite browser! (And with the tests)


# Select from the database all of the TIMES the tweets you collected were posted and fetch all the tuples that contain them in to the variable tweet_posted_times.
q1 = "SELECT time_posted from Tweets"
# print(type(q1))
cur.execute(q1)
tweet_posted_times = cur.fetchall()

# Select all of the tweets (the full rows/tuples of information) that have been retweeted MORE than 2 times, and fetch them into the variable more_than_2_rts.

q2 = "SELECT * from Tweets WHERE retweets > 2"
cur.execute(q2)
more_than_2_rts = cur.fetchall()


# Select all of the TEXT values of the tweets that are retweets of another account (i.e. have "RT" at the beginning of the tweet text). Save the FIRST ONE from that group of text values in the variable first_rt. Note that first_rt should contain a single string value, not a tuple.
q3 = "SELECT tweet_text from Tweets  WHERE instr(tweet_text, 'RT') ORDER BY tweet_text"
cur.execute(q3)
something = cur.fetchone()
first_rt = something[0]
# for item in something:
# 	str(item)
# 	print(item)
# 	print(item[:2])

## Part 3 is a bad test


# Finally, done with database stuff for a bit: write a line of code to close the cursor to the database.

conn.close()

## [PART 3] - Processing data

# Define a function get_twitter_users that accepts a string as in put and returns a SET of the _twitter screennames_ of each twitter user who was mentioned in that string. 
## input: string
## def get_twitter_users(any_string):
     ## 
def get_twitter_users(any_string):
	my_regex = r'@(\w+_?)'
	x = re.findall(my_regex, any_string)
	# My_set = set(x)
	return(set(x))

## return: SET of twitter screennames of each twitter user who was mentioned in that string
## only username if letters and underscores
## regex example tbt
# regex = r'http[s]?://\w+(?:\.\w\w+)+/?\S+'
## this_regex = r'@(\w+_?)'
## must turn a list into tuple 
## return_set = 
## set can't contain list or dictionary, just TUPLES! 
# return_urls = re.findall(regex, any_string)
# Note that the syntax for mentions in a tweet is that the username is preceded by an "@" character, e.g. "@umsi" or "@aadl", and cannot contain any punctuation besides underscores -- that's how to determine what user names are mentioned. (e.g. @hello? is just the username "hello", but @programmer_at_umsi is "programmer_at_umsi"). 

#re.match and getting the 0th group from the MatchObject may be useful for you here... reminder: http://stackoverflow.com/questions/15340582/python-extract-pattern-matches

# You may assume for this problem that there will be no usernames directly in order, e.g. "@hello@goodbye", only "@hello and @goodbye" for example. We will iterate on this later!

# Also note that the SET type is what this function should return, NOT a list or tuple. We looked at very briefly at sets when we looked at set comprehensions last week. In a Python 3 set, which is a special data type, it's a lot like a combination of a list and a dictionary: no key-value pairs, BUT each element in a set is by definition unique. You can't have duplicates.

# If you want to challenge yourself here -- this function definition (what goes under the def statement) CAN be written in one line! Definitely, definitely fine to write it with multiple lines, too, which will be much easier and clearer.





#########
print("*** OUTPUT OF TESTS BELOW THIS LINE ***")

class PartOne(unittest.TestCase):
	def test1(self):
		self.assertEqual(type(umsi_tweets),type([]))
	def test2(self):
		self.assertEqual(type(get_user_tweets("umich")[1]),type({"hi":"bye"}))
	def test3(self):
		fpt = open("206W17_HW7_cache.json","r")
		fpt_str = fpt.read()
		fpt.close()
		obj = json.loads(fpt_str)
		self.assertEqual(type(obj),type({"hi":"bye"}))
	def test4(self):
		self.assertTrue("text" in umsi_tweets[6])
		self.assertTrue("user" in umsi_tweets[4])

class PartTwo(unittest.TestCase):
	def test1(self):
		self.assertEqual(type(tweet_posted_times),type([]))
		self.assertEqual(type(tweet_posted_times[2]),type(("hello",)))
	def test2(self):
		self.assertEqual(type(more_than_2_rts),type([]))
		self.assertEqual(type(more_than_2_rts[0]),type(("hello",)))
	# def test3(self):
	# 	self.assertEqual(set([x[3][:2] for x in more_than_2_rts]),{"RT"})
	def test4(self):
		self.assertTrue("+0000" in tweet_posted_times[0][0])
	def test5(self):
		self.assertEqual(type(first_rt),type(""))
	def test6(self):
		self.assertEqual(first_rt[:2],"RT")
	def test7(self):
		self.assertTrue(set([x[-1] > 2 for x in more_than_2_rts]) in [{},{True}])

class PartThree(unittest.TestCase):
	def test1(self):
		self.assertEqual(get_twitter_users("RT @umsi and @student3 are super fun"),{'umsi', 'student3'})
	def test2(self):
		self.assertEqual(get_twitter_users("the SI 206 people are all pretty cool"),set())
	def test3(self):
		self.assertEqual(get_twitter_users("@twitter_user_4, what did you think of the comment by @twitteruser5?"),{'twitter_user_4', 'twitteruser5'})
	def test4(self):
		self.assertEqual(get_twitter_users("hey @umich, @aadl is pretty great, huh? @student1 @student2"),{'aadl', 'student2', 'student1', 'umich'})


if __name__ == "__main__":
	unittest.main(verbosity=2)
