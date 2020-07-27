# IMPORTS
import requests
import json
import pdfkit 
from bs4 import BeautifulSoup

# VARIABLES
api_url = "https://api.github.com" 
repos = []
features = []
text = ""

# EXECUTION
#Get all repository names from snek-at organization
with requests.get(f"{api_url}/users/snek-at/repos") as repo_req:
    #Convert html response to json
    repo_json = json.loads(repo_req.text)

    for repo in repo_json:
        repos.append(repo["name"])

#Loop through each found repository
for repo in repos:
    #Get all issues from the repository
    with requests.get(f"{api_url}/repos/snek-at/{repo}/issues") as issue_req:
        #Convert html response to json
        issue_json = json.loads(issue_req.text)

        #Filter issues by Feature tag
        for issue in issue_json:
            for label in issue["labels"]:
                if label["name"] == "Feature":
                    features.append(issue["html_url"])

#Loop through each found feature
for feature in features:
    #Get the html code of the feature
    with requests.get(feature) as html_req:
        #Parse the html code with BeautifulSoup
        soup = BeautifulSoup(html_req.text, "html.parser")
        #Get the head of the html code
        head = soup.findAll("head")[0]
        #Get the class with name edit-comment-hide
        issue = soup.find(class_="edit-comment-hide")
        #Combine the head and the issue
        html = f"{str(head)}<body>{str(issue)}</body><div style = 'display:block; clear:both; page-break-after:always;'></div>"
        #Add the html string to the text
        text += html

#Set options for converting html to pdf
"""options = {
    "--header-html": "./header.html"
}"""
#Convert the html text to a PDF file
pdfkit.from_string(text, 'features.pdf')

"""
SPDX-License-Identifier: (EUPL-1.2)
Copyright © Simon Prast
"""