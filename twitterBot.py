﻿import os, sys, random, time
from twitter import *
from param import *
from twitter_keys import *

repliedtweetsits=[]

twitter = Twitter(auth=OAuth(
    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

########################################################################################################
# fonction pour prendre une décision en fonction d'une probabilité
def takeDecision(proba, base):
	decision=random.randint(1, base)
	if decision <proba :
		return True
	else :
		return False
		
# fonction de log
def log(txt,type="INFO"):
	if (verbose==True or type !="INFO") :
		txt="\n"+time.strftime('%d/%m/%y %H:%M',time.localtime())+" : "+type+" - "+txt
		fp = open(LOGFILE, 'a')
		fp.write(str(txt))
		fp.close()

########################################################################################################

log("Let's rock !", "START")

# grab the last ID that the bot replied to, so it doesn't reply to earlier posts. (spam prevention measure)
if os.path.exists(LATESTMFILE):
	fp = open(LATESTMFILE)
	lastid = fp.read().strip()
	fp.close()
	
	if lastid == '':
		lastid = 0
else:
	lastid = 0
	
# Get your "home" timeline
tl=twitter.statuses.home_timeline(since_id=lastid)
log("Parse the timeline")
for tweet in tl:
	if tweet['id'] not in repliedtweetsits :
		log("Section badwords")
		match = set(bad_words) & set((tweet['text'].lower().encode('ascii', 'replace')).split())
		#check if there is a badword in someone's tweets
		if match and twitterName not in tweet['user']['screen_name'].encode('ascii', 'replace'):
			badword=match.pop().upper()
			reply=random.sample(answers,1).pop()
			log("match avec %s" % (badword))
			if takeDecision(70,100) :
			# reply if match
				if reply == 'stoi' :
					try :
						twitter.statuses.update(status="@%s stoi %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()])),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("@%s stoi %s " % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()])),"TWEET")
						time.sleep(1)
					except :
						log("@%s stoi %s " % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()])),"WARNING")
				else :
					try :
						twitter.statuses.update(status="@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),"TWEET")
						time.sleep(1)
					except :
						log("@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),"WARNING")					

		log("Section Boring")
		#check if there is a boring word in someone's tweets
		match = set(boring_words) & set((tweet['text'].lower().encode('ascii', 'replace')).split())
		if match and '@'+twitterName not in tweet['text'].lower() :
			log("match avec %s" % (match))
			if takeDecision(60,100) :
				if tweet['user']['screen_name'].encode('ascii', 'replace') == 'infredwetrust' :
					try :
						twitter.statuses.update(status="@%s TGF" % (tweet['user']['screen_name'].encode('ascii', 'replace')),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("@%s TGF" % (tweet['user']['screen_name'].encode('ascii', 'replace')),"TWEET")
						time.sleep(1)
					except :
						log("@%s TGF" % (tweet['user']['screen_name'].encode('ascii', 'replace')),"WARNING")
				else :
					try :
						twitter.statuses.update(status="TG @%s " % (tweet['user']['screen_name'].encode('ascii', 'replace')),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("TG @%s " % (tweet['user']['screen_name'].encode('ascii', 'replace')),"TWEET")
						time.sleep(1)
					except :
						log("TG @%s " % (tweet['user']['screen_name'].encode('ascii', 'replace')),"WARNING")
				
		
		log("Section OSEF")
		if takeDecision(5,100) :
			try :
				twitter.statuses.update(status="OSEF @%s " % (tweet['user']['screen_name'].encode('ascii', 'replace')) ,in_reply_to_status_id=tweet['id'])
				repliedtweetsits.append(tweet['id'])
				log("OSEF @%s " % (tweet['user']['screen_name'].encode('ascii', 'replace')),"TWEET")
				time.sleep(1)
			except :
				log("OSEF @%s " % (tweet['user']['screen_name'].encode('ascii', 'replace')),"WARNING")
		
		
		
mt=twitter.statuses.mentions_timeline(since_id=lastid)
log("Parse the mentions")
for tweet in mt:
	log("Section Mentions")
	if tweet['id'] not in repliedtweetsits :
		match = set(tg_list) & set((tweet['text'].lower().encode('ascii', 'replace')).split())
		if match and twitterName not in tweet['user']['screen_name'].encode('ascii', 'replace') :
			badword=match.pop().upper()
			reply=random.sample(answers,1).pop()
			log("match avec %s" % (reply))
			if takeDecision(90,100) :	
				if reply == 'stoi' :
					try :
						twitter.statuses.update(status="@%s stoi %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()])),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("@%s stoi %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()])),"TWEET")
						time.sleep(1)
					except :
						log("@%s stoi %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()])),"WARNING")
				else :
					try :
						twitter.statuses.update(status="@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),"TWEET")
						time.sleep(1)
					except :
						log("@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),"WARNING")					
			elif takeDecision(1,100) :
				log("On laisse passer le tweet" ,"TWEET")
				repliedtweetsits.append(tweet['id'])


		log("Section badwords")
		match = set(bad_words) & set((tweet['text'].lower().encode('ascii', 'replace')).split())
		if match and twitterName not in tweet['user']['screen_name'].encode('ascii', 'replace') :
			badword=match.pop().upper()
			reply=random.sample(answers,1).pop()
			log("match avec %s" % (badword))
			if takeDecision(50,100) :
				if reply == 'stoi' :
					try :
						twitter.statuses.update(status="@%s stoi %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()]) , (badword)),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("@%s stoi %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()]) ),"TWEET")
						time.sleep(1)
					except :
						log("@%s stoi %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (bad_words[badword.lower()]) ),"WARNING")
				else :
					try :
						twitter.statuses.update(status="@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),in_reply_to_status_id=tweet['id'])
						repliedtweetsits.append(tweet['id'])
						log("@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),"TWEET")
						time.sleep(1)
					except :
						log("@%s %s" % (tweet['user']['screen_name'].encode('ascii', 'replace') , (reply) ),"WARNING")					
			elif takeDecision(1,100) :
				log("On laisse passer le tweet" ,"TWEET")
				repliedtweetsits.append(tweet['id'])

log("Section Ranom Tweet")
reply=random.sample(talk,1).pop()
if takeDecision(15,100) :
	try :
		twitter.statuses.update(status="%s" % (reply) ,in_reply_to_status_id=tweet['id'])
		log("%s" % (reply),"TWEET")
	except :
		log("%s" % (reply),"WARNING")	
				
if repliedtweetsits :
	fp = open(LATESTMFILE, 'w')
	fp.write(str(max(repliedtweetsits)))
	fp.close()

log("An other job is done.", "STOP")