
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

    # we can also cleanup the bodyHtml column to remove all the <p> and <\p> tags
    df["bodyHtml"] = df["bodyHtml"].apply(lambda x: re.sub("<p[^>]*>", "", x).replace("</p>", ""))
    # we can also remove the <a> and </a> tags.  The stuff inside the <a> tags is still to be shown, but the <a> tags (including href attributes) themselves are removed
    df["bodyHtml"] = df["bodyHtml"].apply(lambda x: re.sub("<a[^>]*>", "", x).replace("</a>", ""))

    print(df.head())

    tag = re.sub(r'[\\/:"*?<>|]+', '', tag)
    df.to_csv(f"data/guardian_articles_{tag}.csv", index=False)


query_and_save_dataframe('environment/energy', '1', '2022-01-01')