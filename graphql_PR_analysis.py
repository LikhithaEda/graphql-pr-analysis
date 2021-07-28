from python_graphql_client import GraphqlClient
import requests
import json
import pandas as pd
from pandas import json_normalize
from string import Template
import numpy as np



headers = {"Authorization": "token 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"}


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200: #200 means request fulfilled
        return request.json()
        #return request.text
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

#client = GraphqlClient(endpoint="https://api.github.com/graphql")

def build_query(pr_cursor):
  if pr_cursor is None:
        return ''
  return Template("""
  query($cursor:String!){
    repository(owner: "redhat-openshift-ecosystem", name: "operator-test-playbooks") {
      pullRequests(first: 15, after: $cursor) {
        pageInfo{
          hasNextPage
          endCursor
        }
        edges {
          node {
            author {
              login
            }
            mergedBy {
              login
            }
            createdAt
            mergedAt
            autoMergeRequest {
              enabledBy {
                login
              }
              mergeMethod
            }
          }
        }
      }
    }
  }
  """).substitute({'cursor': pr_cursor})
  

"""
result = run_query(query)  
data_frame = pd.json_normalize(result['data']['repository']['pullRequests']['edges'])
page_info = pd.json_normalize(result['data']['repository']['pullRequests']['pageInfo'])
print(data_frame)
print(page_info)
cursor = page_info.loc[0,'endCursor']
print(cursor)
"""

def get_PR_data():
  cursor = "null"
  hasNextPage = True
  while (hasNextPage == True):
    getPRinfo = build_query(cursor)
    result = run_query(getPRinfo)  
    print(result)
    data_frame = pd.json_normalize(result['data']['repository']['pullRequests']['edges'])
    page_info = pd.json_normalize(result['data']['repository']['pullRequests']['pageInfo']) 
    print(data_frame)
    #print(page_info)
    cursor = page_info.loc[0,'endCursor'] #update cursor
    hasNextPage = page_info.loc[0,'hasNextPage'] #update hasNextPage
    

#Create a function to append to the dataframe for each pagination
#df = df.drop('column_name', 1)
#where 1 is the axis number (0 for rows and 1 for columns.)
#def main(argv):
  #get data from the graphql query
get_PR_data()