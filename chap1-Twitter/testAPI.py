# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 23:32:56 2015

@author: chris
"""

import twitter
import json
from prettytable import PrettyTable
from collections import Counter

CONSUMER_KEY='mAjUCPtzt3ni1OdLVwDDVApIY'
CONSUMER_SECRET='1rF90lkOo4mB8d5k0Lul6NHpmYeyjx4plZxEUzeRgcPIgHEvtQ'
OAUTH_TOKEN='274111062-TbPPvN0NKlV8nS7KXnTZLsadleYgc44rSyMtHcL9'
OAUTH_TOKEN_SECRET='ohxRD3OWgflfdNozfxy5dfyNgWt5GdliI5Hs3XbU4uqYx'
auth=twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api=twitter.Twitter(auth=auth)

WORLD_WOE_ID=1
US_WOE_ID=23424977



world_trends=twitter_api.trends.place(_id=WORLD_WOE_ID)
us_trends=twitter_api.trends.place(_id=US_WOE_ID)
#print json.dumps(us_trends, indent=1)
world_trends_set=set([trend['name']
                        for trend in world_trends[0]['trends']])
us_trends_set=set([trend['name']
                        for trend in us_trends[0]['trends']])
common_trends=world_trends_set.intersection(us_trends_set)
#print json.dumps(us_trends, indent=1)

q='@ANEOConseil'

count=100

search_results= twitter_api.search.tweets(q=q,count=count)

statuses=search_results['statuses']

status_texts=[status['text']for status in statuses]
print json.dumps(status_texts,indent=1)

screen_names=[user_mention['screen_name']for status in statuses
                for user_mention in status['entities']['user_mentions']]
                    
                    
hashtags=[hashtag['text']
            for status in statuses
                for hashtag in status['entities']['hashtags']]                    
print json.dumps(screen_names,indent=1)                       
print json.dumps(hashtags, indent=1)
words=[w for t in status_texts
            for w in t.split()]
for item in [words,screen_names,hashtags]:
    c=Counter(item)
    print c.most_common()[:10]

for label, data in (('Word',words),
                    ('Screen Name',screen_names),
                    ('Hashtag',hashtags)):
    pt=PrettyTable(field_names=[label,'Count'])
    c=Counter(data)
    [pt.add_row(kv) for kv in c.most_common()[:10]]
    pt.align[label],pt.align['Count']='l','r'
    print pt
    
    
#A function for computing lexical diversity
def lexical_diversity(tokens):
    return 1.0*len(set(tokens))/len(tokens)

def average_words(statuses):
    total_words=sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)

print lexical_diversity(words)
print lexical_diversity(screen_names)
print lexical_diversity(hashtags)
print average_words(status_texts)
