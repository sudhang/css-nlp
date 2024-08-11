
import pandas as pd
import re
import os
import requests

def query_api(tag, page, from_date, api_key):
    """
    Function to query the API for a particular tag
    returns: a response from API
    """
    response = requests.get("https://content.guardianapis.com/search?tag="
                            + tag + "&from-date=" + from_date 
                            +"&page=" + str(page) +  "&show-blocks=body&page-size=200&api-key=" + api_key)
    return response

def query_and_save_dataframe(tag, page, from_date):

    response = query_api(tag, page, from_date, 'd92a21c1-3798-4079-8290-82f18947f8b3')
    df = pd.json_normalize(response.json()['response']['results'])

    df["bodyHtml"] = df["blocks.body"].apply(lambda x: x[0]['bodyHtml'])

    # we now only want to keep the columns id, type, sectionId, sectionName, webPublicationDate, webTitle, webURL, bodyHtml
    df = df[["id", "type", "sectionId", "sectionName", "webPublicationDate", "webTitle", "webUrl", "bodyHtml"]]

    # we can also cleanup the bodyHtml column to remove all the html tags
    df["bodyHtml"] = df["bodyHtml"].apply(lambda x: re.sub("<\/?[^>]*>", "", x))

    print(df.head())

    tag = re.sub(r'[\\/:"*?<>|]+', '__', tag)
    df.to_csv(f"data/guardian_articles_{tag}.csv", index=False)


query_and_save_dataframe('environment/energy', '1', '2022-01-01')