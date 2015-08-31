#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Made by will beddow with the help of sulav khadka
import urllib2, urllib, json, re, wikipedia, wolframalpha
#import TTS_Talk
import json as m_json
import os
import __builtin__
import say
import wcycle
import requests
def urlparse(url, searchterm, user):
#Not working yet, will go into urls and search for results.
	termsplit = searchterm.split(" ")
	for word in termsplit:
		r = requests.get(url)
		rt = r.text
		try:
			#First split the text from the search term
			rto = rt.split(word)
			#Next search for the most recent html tag
			rtp = rto[0].split('>')
			#Next get everything ahead of that to the search term
			firsttoterm = rtp[1]
			#Next get the last html tag
			rtn = rto[1].split('<')
			#Next get everything behind that to the search term
			lasttoterm = rtn[0]
			finalresult = firsttoterm+word+lasttoterm
			print(finalresult)
		except IndexError:
			pass
def wlfram_search(user_query, user, appid):
	try:
		client = wolframalpha.Client(appid)
		res = client.query(user_query)
		if next(res.results).text != 'None':
			#for i in res.pods:
				#print "\n"
				#print i.text
#			phrase = str(next(res.results).text)
#			TTS_Talk.tts_talk(phrase)
			print(next(res.results).text)
		else:
			google_search(user_query, user)
	except StopIteration: 
		google_search(user_query, user)	

def skwiki(titlequery, user):
	result = wikipedia.summary(titlequery, sentences=2)
	print(result)

def print_gsearch(results, user, searchterm):
	phrase = "I was unable to find an answer. Here are some links on the subject"
	#TTS_Talk.tts_talk(phrase)
        for result in results:
        	title = result['title']
		url = result['url']
		pattern = re.compile('<.*?>')
		title = re.sub(pattern,'',title)
#		Uncomment the below line and comment the one under it to reenable the broken urlparse function
#		urlparse(url, searchterm, user)
		print(title+': '+url)

def google_search(user_query, user):
	query = user_query
        query = urllib.urlencode ( { 'q' : query } )
        response = urllib2.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
        json = m_json.loads ( response )
       	results = json [ 'responseData' ] [ 'results' ]
	wiki_bool = False
        for result in results:
        	title = result['title']
		url = result['url']
		pattern = re.compile('<.*?>')
		title = re.sub(pattern,'',title)
		if "Wikipedia, the free encyclopedia" in title:
			titlelst = title.split('-')
			titlequery = titlelst[0].strip()
			skwiki(titlequery, user)
			wiki_bool = True
			break
			
	if wiki_bool == False:
		print_gsearch(results, user, user_query)
		
			
def main(query, user, appid):
	wlfram_search(query, user, appid)
#start main with an appid or uncomment the below line
#appid = raw_input("Please enter a wolframalpha app id")
