#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:23:39 2017

@author: adamnicolaspelletier
"""

import json
import urllib
import urllib2

def read_webhose_key():
    """
    Reads the Webhose API key from a file called 'search.key'.
    Returns either None (no key found), or a string representing the key. 
    Remember: put search.key in your .gitginore file to avoid committing it!
    """
     
    webhose_api_key = None
    
   
    try:
        with open('search.key', 'r') as f:
            webhose_api_key = f.readline().strip()
    except IOError:
        try: 
            with open('../search.key', 'r') as f:
                webhose_api_key = f.readline().strip()
        except: 
            raise IOError('search.key file not found')
    
    return webhose_api_key

def run_query(search_terms,size=10):
    """Given a string containing search terms (query), and a number of results to 
    return (default of 10), returns a list of results from the Webhose API,
    with each result consisting of a title, link and summary.
    """
        
    webhose_api_key = read_webhose_key()
    
    if not webhose_api_key:
        raise KeyError('Webhose key not found')
    # Whats the base URL for the Webhose API?
    root_url = 'http://webhose.io/search'
    
    #Format the querystring - escape special characters.
    query_string = urllib.quote(search_terms)
    
    #Use string formatting to construct the complete API URL.
    # search_url is a string split over multiple lines.
    search_url = ('{root_url}?token={key}&format=json&q={query}'
                  '&sort=relevancy&size={size}').format(
                          root_url=root_url,
                          key=webhose_api_key,
                          query=query_string,
                          size=size)
    results =  []
    
    try:
        #Connect to the Webhose API, and convert the response to a 
        #Python dictionary.
        response = urllib2.urlopen(search_url).read()
        json_response = json.loads(response)
        
        #Loop through the posts, appending each to the results list as
        # a dictionary. We restrict the summry to the first 200
        # characters, as summary responses from Webhose can be long!
        for post in json_response['posts']:
            results.append({'title':post['title'],
                        'link':post['url'],
                        'summary':post['text'][:200]})
    except:
        print("Error when querying the Webhose APOI")
    
    #Return tje list of results to the calling function.
    return results


 # Start execution here!
if __name__ == '__main__':
    search_terms = raw_input("What are your search terms for the Webhose API?  ")
    
    for i in run_query(search_terms,size=10):
        print i["title"]
        print i["link"]
        print i["summary"]
        print ""
        