import requests
import json
import html
import re

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
    products(sortKey: TITLE, first: 1) {
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
    products(sortKey: TITLE, first: 1 after: "{cur}") {{
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
counter = 1
changed = 0

hasNextPage = True
while(hasNextPage):
  product = result["data"]["products"]
  hasNextPage = product["pageInfo"]["hasNextPage"]
  cursor = product["edges"][0]["cursor"]
  prodNode = product["edges"][0]["node"]
  descriptionOrig = prodNode["descriptionHtml"]
  prodId = prodNode["id"]
  title = prodNode["title"]

  print(f"{counter}: {title}")

  # Rules for altering the description
  # These are regular expressions - use https://regex101.com/ to help write them
  # The structure is [("regex1", "replacement1"), ("regex2", "replacement2")...]
  changes = [
    ("Absolute Medical Equipment \(A.M.E. Ultrasounds\) is proud", "We are proud")
  ]

  descriptionNew = descriptionOrig
  for change in changes:
    toAlter = change[0]
    alteration = change[1]
    if(re.search(toAlter, descriptionOrig, flags=re.I)):
      print(f"Found match for '{toAlter}'...")
      descriptionNew = re.sub(toAlter, alteration, descriptionOrig, flags=re.I)

  if (descriptionNew != descriptionOrig):
    print("Sending updated description...")
    result = ChangeProdDesc(prodId, descriptionNew)
    changed += 1
    print("Done.")
  else:
    print("No changes made!")

  print()

  if(hasNextPage):
    counter += 1
    result = GetNextProduct(cursor)
  else:
    print(f"Finished going through all {counter} products!")
    print(f"Changed the descriptions on {changed} products.")
