import requests
import json
import html

from dotenv import load_dotenv
load_dotenv()
import os

access_token = os.getenv("access_token")
headers = {
  "X-Shopify-Access-Token": access_token
}
url = os.getenv("url")

def GetFirstProduct():
  query = """
  {
    products(first: 1) {
      pageInfo {
        hasNextPage
      }
      edges {
        cursor
        node {
          title
          id
          descriptionHtml
        }
      }
    }
  }
  """

  request = requests.post(url, json={'query': query}, headers=headers)
  return(request.json())

def GetNextProduct(cursor):
  query = """
  {{
    products(first: 1 after: "{cur}") {{
      pageInfo {{
        hasNextPage
      }}
      edges {{
        cursor
        node {{
          title
          id
          descriptionHtml
        }}
      }}
    }}
  }}
  """.format(cur = cursor)

  request = requests.post(url, json={'query': query}, headers=headers)
  return(request.json())

def ChangeProdDesc(prodId, desc):

  input = f'{{ id: "{prodId}", descriptionHtml: """{desc}""" }}'
  # print(input)

  mutation = """
  mutation productUpdate {{
    productUpdate(input:
      {input}
    ) {{
      product {{
        title
        descriptionHtml
      }}
      userErrors {{
        field
        message
      }}
    }}
  }}
  """.format(input = input)

  request = requests.post(url, json={'query': mutation}, headers=headers)
  return(request.json())

result = GetFirstProduct()

product = result["data"]["products"]
hasNextPage = product["pageInfo"]["hasNextPage"]
cursor = product["edges"][0]["cursor"]
prodNode = product["edges"][0]["node"]
description = prodNode["descriptionHtml"]
prodId = prodNode["id"]
title = prodNode["title"]

counter = 1
print(f"{counter}: {title}")
# print(description)

# Regular expressions for altering the description

result = ChangeProdDesc(prodId, description)
print(result)

# while(hasNextPage):
#   result = GetNextProduct(cursor)

#   product = result["data"]["products"]
#   hasNextPage = product["pageInfo"]["hasNextPage"]
#   cursor = product["edges"][0]["cursor"]
#   prodNode = product["edges"][0]["node"]
#   description = prodNode["descriptionHtml"]
#   prodId = prodNode["id"]
#   title = prodNode["title"]
#   counter += 1
#   print(f"{counter}: {title}")