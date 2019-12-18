import requests
import json

access_token = "864860e8fa191548d478eb6f64673c38"
headers = {
  "X-Shopify-Access-Token": access_token
}
url = 'https://absolute-medical-equipment.myshopify.com/admin/api/2019-10/graphql.json'

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
          descriptionHtml
        }}
      }}
    }}
  }}
  """.format(cur = cursor)

  request = requests.post(url, json={'query': query}, headers=headers)
  return(request.json())

result = GetFirstProduct()

product = result["data"]["products"]
hasNextPage = product["pageInfo"]["hasNextPage"]
cursor = product["edges"][0]["cursor"]
prodNode = product["edges"][0]["node"]
description = prodNode["descriptionHtml"]
title = prodNode["title"]

counter = 1

print(f"{counter}: {title}")

while(hasNextPage):
  result = GetNextProduct(cursor)

  product = result["data"]["products"]
  hasNextPage = product["pageInfo"]["hasNextPage"]
  cursor = product["edges"][0]["cursor"]
  prodNode = product["edges"][0]["node"]
  description = prodNode["descriptionHtml"]
  title = prodNode["title"]
  counter += 1
  print(f"{counter}: {title}")