import requests
import json
import pdfkit 
from bs4 import BeautifulSoup

api_url = "https://api.github.com" 
repos = []
features = []
html = ""

with requests.get(f"{api_url}/users/snek-at/repos") as repo_req:
    repo_json = json.loads(repo_req.text)
    for repo in repo_json:
        repos.append(repo["name"])

for repo in repos:
    with requests.get(f"{api_url}/repos/snek-at/{repo}/issues") as issue_req:
        issue_json = json.loads(issue_req.text)
        for issue in issue_json:
            for label in issue["labels"]:
                if label["name"] == "Feature":
                    features.append(issue["html_url"])

for feature in features:
    with requests.get(feature) as html_req:
        soup = BeautifulSoup(html_req.text, "html.parser")
        issue = soup.find(class_="edit-comment-hide")
        html += str(issue)

pdfkit.from_string(html, 'features.pdf')