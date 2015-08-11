#!/usr/bin/env python3
##########################################
# (c)2015
# Thomas Middleton    
# thomas.g.middleton@gmail.com
# 
import urllib.request
import json


##########################################
##########################################

def getRepos(keyword, numberOfRepositories):
  """
getRepos
This function returns a list of repositories based on search criterion.
Inputs:
keyword               - search query
numberOfRepositories  - Number of repositories requested
Returns:
JSON object
  """
  #Main application

  #Sort by forks and descending
  sortBy='forks'
  sortOrder='desc'

  #This is a dictionary we will make JSON later
  retDict  = {'keyword_searched':         keyword,
              'desired_number_of_repos':  numberOfRepositories,
              'number_of_repos_returned': None,
              'list_of_repos':            []}


  #https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}
  searchQuery = "https://api.github.com/search/repositories?q={query}&page={page}&per_page={per_page}&sort={sort}&order={order}"

  #by default, set to requested number, will update later.
  retDict['number_of_repos_returned'] = numberOfRepositories

  pageNumber = 1
  while (len(retDict['list_of_repos']) < retDict['number_of_repos_returned']):
    #loop through and gather 100 at a time
    searchURL = searchQuery.format(query=keyword, page= pageNumber, per_page = 100, sort=sortBy, order=sortOrder)

    #read URL, decode as uft-8, decode from JSON to Python
    repoSearchData = json.loads(urllib.request.urlopen(searchURL).read().decode('utf-8'))

    if repoSearchData['total_count'] < numberOfRepositories:
      #Are we asking for more than we found?
      retDict['number_of_repos_returned'] = repoSearchData['total_count']

    pageNumber += 1
    for repo in repoSearchData['items']:
      #Easy way to do this, but not very pretty.
      repoDict = {}
      repoDict['id'] =                  repo['id']
      repoDict['name'] =                repo['name']
      repoDict['description'] =         repo['description']
      repoDict['language'] =            repo['language']
      repoDict['created_date'] =        repo['created_at']
      repoDict['html_url'] =            repo['html_url']
      repoDict['number_of_watchers'] =  repo['watchers_count']
      repoDict['number_of_forks'] =     repo['forks']
      repoDict['owner_username'] =      repo['owner']['login']
      repoDict['owner_id'] =            repo['owner']['id']
      repoDict['owner_html_url'] =      repo['owner']['html_url']

      #Appending to the list, must use dict because python doesn't make hardcopy of Dict objects
      retDict['list_of_repos'].append(dict(repoDict))

      if len(retDict['list_of_repos']) == retDict['number_of_repos_returned']:
        #Since we are getting 100 hits per page, if the last page has more than we need, stop short.
        break
    

  retJSONdict = json.JSONEncoder().encode(retDict)
  #encode and return
  return retJSONdict

  

if __name__ == "__main__":
  import argparse
  argumentParser = argparse.ArgumentParser(description='GitHub Query')
  argumentParser.add_argument('keyword', type=str, nargs=1, help='Repository search keyword')
  argumentParser.add_argument('RepositoryCount', type=int, nargs=1, help='Desired number of repositories.')
  arguments = argumentParser.parse_args()
  print(getRepos(arguments.keyword[0], arguments.RepositoryCount[0]))
